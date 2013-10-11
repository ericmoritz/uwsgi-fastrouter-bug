# UWSGI fastrouter lockup

There appears to be a bug introduced in UWSGI 1.9 that causes the fastrouter to
lock up when loaded down with requests with a Cookie header value that is some where
around 3k and 4k.

The observed behavior in strace is that the fastrouter reads the request from nginx
and it fails to write those bytes to the backend.

I have used git bisec to narrow down the bug to the following commits:

```
94c29a396a405649200c3add11630a18b0a4ea43
bba8e503c1fbcc64ec1cd50aedf2405a104575a4
9c2e9e42f95f9963eab547916b5ba08486450da5
82d5e0ead8e8aea39786e6d4d03e3bce4cc111b7
1004ad0edcaa1be35bd5983e90312a8ac1e1e13f
688a2278860089590a5af204da86fd2204609a03
```

I suspect that the `688a` commit introduced the bug as it is the only commit
that touches the corerouter code. However `688a` does not compile but `94c2` does.

[Github changeset](https://github.com/unbit/uwsgi/compare/7541195a5f7504a3782a110d71b973fd570ae3f0...94c29a396a405649200c3add11630a18b0a4ea43)


## Install

To provision the Ubuntu 12.04 box do the following:

    vagrant up

## Running

In one shell do the following:

    vagrant ssh
    cd /vagrant
    src/uwsgi/uwsgi --ini uwsgi.ini

In another do the following:

    vagrant ssh
    cd /vagrant
    python test.py

If the test stops after 30s the bug exists, if the test stops after 60s the bug is
not there.

