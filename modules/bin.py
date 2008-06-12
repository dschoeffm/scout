import scout
import sys
# import zypp

# class ZyppParser(object):
# 
#     rebuild_cache = False
# 
#     @classmethod
#     def list(cls):
#         z = zypp.ZYppFactory_instance().getZYpp()
#         repoManager = zypp.RepoManager()
#         repos = repoManager.knownRepositories()
# 
#         for repo in repos:
#             if not repo.enabled():
#                 continue
#             if cls.rebuild_cache and not repoManager.isCached(repo):
#                repoManager.buildCache(repo)
#             z.addResolvables(repoManager.createFromCache(repo).resolvables())
# 
#     print "Available items: %d" % ( z.pool().size() )
#     for item in z.pool():
#         print "* %s:%s-%s.%s\t(%s)" % ( item.resolvable().kind(),
#                                         item.resolvable().name(),
#                                         item.resolvable().edition(),
#                                         item.resolvable().arch(),
#                                         item.resolvable().repository().info().alias() )

install_cmd = "sudo zypper install";

paths = [ "/bin", "/sbin", "/usr/bin", "/usr/sbin", "/usr/games", "/opt/kde3/bin", "/opt/kde3/sbin", "/opt/gnome/bin", "/opt/gnome/sbin" ];

class ScoutModule(object):

    name = "bin"
    desc = "Search for the binaries contained in the packages."

    @classmethod
    def query_zypp(cls, term):
        # TODO: implement
        print "Querying zypp repositories is not yet implemented"
        return None

    @classmethod
    def query_repo(cls, repo, term):
        db = scout.Database(cls.name + '-' + repo)
        r = db.execute('SELECT binary, path, package FROM binary LEFT JOIN path ON binary.id_path=path.id_path LEFT JOIN package ON binary.id_pkg=package.id_pkg WHERE binary=?', term)
        result = scout.Result( ['bin', 'path', 'pkg'], ['binary', 'path', 'package']);

        if isinstance(r, list):
            for rr in r:
                result.addrow(rr)
        else:
           result.addrow(r)
        return result

    @classmethod
    def main(cls):

        p = scout.Parser(cls.name)
        p.add_repo('zypp')
        p.add_repos_from_datadir()
        if not p.parse():
            return None
        repo = p.options.repo

        term = p.args[0]

        if repo == 'zypp':
            return cls.query_zypp(term)
        else:
            return cls.query_repo(repo, term)