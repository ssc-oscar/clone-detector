import csv
import sys
import gzip
from collections import defaultdict
import tqdm

# Pick off the suffix of the filename
def filekind(fn):
    fn = fn.split("/")[-1]
    if "." in fn:
        return fn.lower().split(".")[-1]
    else:
        return fn
        
kinds = dict()

# 1. what % of copies are R files
# 2. what % of R files are by different author
#    (interesting because a common case seems to be an author
#     who puts the same file in multiple of their own projects,
#     but others do not do this).

kount = 0
kount_r = 0
kount_r_different = 0
cloner_projects = defaultdict(set)  # set of project-file-date from which stuff was cloned into project
#config = (["go"], "data/clones_go.csv.gz", "Go-repos.txt")
#config = (["r"], "data/clones_cran.csv.gz", "CRAN-repos.txt")
#config = (["rs","rlib","rst"], "data/clones_rust.csv.gz", "Cargo-repos.txt")
#config = (["js"], "clones_npm.csv.gz", "NPM-repos.txt")
#validkinds = config[0]
#clonefile = config[1]
#repolist = config[2]
validkinds = sys.argv[1].split(",")   # comma-separated list of suffixes
repolist = sys.argv[2]                # List of repos part of ecosystem
clonefile = sys.argv[3]               # Output file of clone_detector3.py

print "   (out of ", len(open(repolist).readlines()), "projects)"

kinds = dict()

for row in tqdm.tqdm(csv.reader(gzip.open(clonefile))):
    try:
        from_prj,from_fn,from_date,from_author,\
        to_prj,to_fn,to_date,to_author,blob_length,\
        to_commit_id = row
    except:
        print "Failed to parse ", row
        continue

    # This is for a study about ecosystem behavior in 2016
    if not to_date.startswith("2016"): 
        continue

    kind = filekind(from_fn) 
    if kind not in kinds: kinds[kind] = set()
    kinds[kind].add(from_prj + ":" + from_fn) 
    sameowner = from_prj.split("_")[0] == to_prj.split("_")[0]
    kount += 1
    if kind in validkinds:
        cloner_projects[to_prj].add(  from_prj + "--" + from_fn + "--" + from_date )
    if kind in validkinds: kount_r += 1
    if kind in validkinds and not sameowner: 
        kount_r_different += 1


print "out of ", kount, "cloned files,", kount_r, "are (", "/".join(validkinds),") files", "and of those only", kount_r_different, "crossed owner/org boundaries"
print "There were", len(cloner_projects), " projects that cloned on average", 
print sum([len(cloner_projects[cp]) for cp in cloner_projects]) / len(cloner_projects) , "files"
print "A few examples:"
for cp in list(cloner_projects.keys())[:10]:
    print cp, len(cloner_projects[cp]), "\n\t".join(list(cloner_projects[cp])[:5])
print "Invalid kinds"
for k in sorted(kinds.keys()):
    if len(kinds[k]) > 5:
        print k,len(kinds[k]),list(kinds[k])[:5]
