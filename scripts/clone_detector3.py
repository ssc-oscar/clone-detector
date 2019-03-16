from oscar import *
import glob
import pickle
import re
import gzip
import csv
import sys
import argparse
from dateutil.parser import parse
from datetime import datetime
import pdb

currentblob = ""
projecttimes = dict()

repos = sys.argv[1]     # File with list of repositories in form owner_name
outfile = sys.argv[2]   # CSV file to write results
maps = sys.argv[3]      # Template file name for "map" files

# NB Map files are 32 compressed files containing lists of blobs in 
#  a particular language, with commit, project, author, and date.
#  These are sorted by blob id (a 40-char SHA-1 string)
#  A blob may be listed several times, and we are looking for
#  places where the same blob is committed to multiple projects
#  in the same ecosystem; this may be evidence of cloning

candidates = {prj.strip().lower() for prj in open(repos)}

clones = csv.writer(gzip.open(outfile, "w"))
clones.writerow(["from_prj","from_date","from_author","to_prj","to_date","to_author","blob_length","to_commit_id"])

# Look up the filename that a particular commit used for this blob
def cmtNblob2filename(cmt,blob):
  try:
    files = Commit(cmt).tree.files
    for f in files:
        if files[f] == blob: return f
    return "(unknown)"
  except ObjectNotFound, e:
    return "(oscar error)"
  

# Given a blob's SHA and a list of (time, author, commit) instances,
# 
# Output a line to the csv file
#    linking the earliest instance within our set of repos
#    to each later instance inside the time frame we're interested in
# 
def dump(blobid, projecttimes):

    # If there's only one blob, no cloning happened
    if len(projecttimes.keys()) < 2: return
    print ".",
    cmts = [cmt for (when,who,cmt) in projecttimes.values()]

    # find the earliest example of the blob
    (srcprj,(srcwhen,srcwho,srccmt)) = min(projecttimes.items(), key=lambda (proj,(when,who,cmt)): when)

    whent = datetime.fromtimestamp(float(srcwhen)).isoformat()
    bloblen = 0
    srcfilename = cmtNblob2filename(srccmt,blobid)
    try:
        bloblen = len(Blob(blobid).data)
    except Exception, e:
        pass #print "Blob length: ", e
    
    for prj in projecttimes:
        if prj != srcprj:
            to_whent = datetime.fromtimestamp(float(projecttimes[prj][0])).isoformat()
            to_fn = "(not looked up)" #cmtNblob2filename(projecttimes[prj][2], blobid)
            clones.writerow([srcprj, srcfilename, whent, srcwho, prj, to_fn, to_whent, projecttimes[prj][1], bloblen,projecttimes[prj][2]])
            
        
# For each of the 32 map files, search
# for a set of rows about the same blob, and analyze them
#  for ecosystem-specific cloning behaviors
for sfile in [maps % (k,) for k in range(0,32)]:
    print "Reading", sfile
    for row in gzip.open(sfile):
        blob,cmt,proj,when,who = row.strip().split(";")

        # Skip stuff newer than 2017-01-01; this is for a 
        # study about ecosystem activity in 2016
        if int(when) > 1483228800: continue   
        if proj.lower() not in candidates: 
            continue
        if blob != currentblob:
            dump(currentblob, projecttimes)
            currentblob = blob
            projecttimes = {proj: (when,who,cmt)}
        else:
            if proj in projecttimes and projecttimes[proj][0] > when:
                projecttimes[proj] = (when,who,cmt)
            elif proj not in projecttimes:
                projecttimes[proj] = (when,who,cmt)
    dump(currentblob, projecttimes)
     
