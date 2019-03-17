
# Scripts for detecting clones within software ecosystems

## clone_detector3.py: Detect relevant clones

Given a list of blobs in a particular language, and the commits
those blobs are found in, find a list of relevant blob pairs for this
ecosystem.

The list of blobs (/data/play/<language>thrumaps/) is created as part of trend and dependency calculation mentioned in https://github.com/ssc-oscar/plots ("see grepNew.pbs and overview/deps/b2pkgs...")

(See also https://github.com/ssc-oscar/fingerprinting)

ex: `clone_detector3.py Go-repos.txt clones_go.csv.gz /data/play/GothruMaps/b2cPtaKGo.%d.s'`

### Sample output:

```
from_prj,from_date,from_author,to_prj,to_date,to_author,blob_length,to_commit_id
enj_origin,pkg/registry/pod/etcd/etcd.go,2015-05-01T12:19:44,Eric Paris <eparis@
redhat.com>,nqn_kubernetes-mesos,Godeps/_workspace/src/github.com/GoogleCloudPla
tform/kubernetes/pkg/registry/pod/etcd/etcd.go,2015-05-19T18:58:08,James DeFelic
e <james.defelice@gmail.com>,11608,913f2d251c6a7abb0367a0b81fff7ed351c94066
enj_origin,pkg/auth/authenticator/token/cache/cache_test.go,2015-09-30T14:29:08,
Jordan Liggitt <jliggitt@redhat.com>,fabric8io_configmapcontroller,vendor/github
.com/openshift/origin/pkg/auth/authenticator/token/cache/cache_test.go,2016-10-2
1T06:32:10,rawlingsj <rawlingsj80@gmail.com>,4950,d824a09608de80637612117fbf1133
8630325755
```


## post_analyze_clones.py

Collect statistics and examples about the clones

ex: `post_analyze_clones.py go Go-repos.txt data/clones_go.csv.gz`

## Sample output

```
out of  2819834 cloned files, 2803786 are ( go ) files and of those only 2748026
 crossed owner/org boundaries
There were 16905  projects that cloned on average 165 files
A few examples:
howeyc_servedir 9 nyaxt_otaru--Godeps/_workspace/src/github.com/gorilla/mux/rege
xp.go--2015-08-12T09:52:56
    cyph_cyph--default/github.com/gorilla/mux/doc.go--2015-08-13T22:44:14
    cyph_cyph--default/github.com/gorilla/mux/old_test.go--2015-08-13T22:44:
14
    johnworth_jobrunner--_vendor/src/github.com/gorilla/context/context.go--
```
