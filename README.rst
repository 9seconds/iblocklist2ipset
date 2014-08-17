iblocklist2ipset
=========

|Build Status| |Coverage Status| |Health Status|

iblocklist2ipset is a small utility (really small, check out sources)
to manage your favourite `iblocklists <https://www.iblocklist.com/>`__
with `IPSets <http://ipset.netfilter.org/>`__.

All it does, it converts lists from P2P format to the format compatible with
``ipset restore``. Basic usage is following:

::

    $ iblocklist2ipset generate \
        --ipset idiots
        "http://list.iblocklist.com/?list=usrcshglbiilevmyfhse&fileformat=p2p&archiveformat=gz" \
        > ~/.ipset
    $ sudo ipset restore -f ~/.ipset

And you are done.

Now let's try to figure out why do you need it (and you need it).


Why do you need it
------------------

Let's imagine you are living in a country where DMCA makes sense and you
want to make your seedbox safe but you can't use PeerGuardian or PeerBlock
because it sucks on Linux so you decide to use iptables + ipset so...

Wait. It looks like a tool for... piracy? No, of course it is not. Let's start
again.

Let's imagine you have some kind of server (bare metal or cloud VM) and you are
running some mission critical software on it. You do not like botnets or EVIL HACKERS
so want to block all of them to have some good feeling of safety. You heard about
blocklists supplied by `BlueTack <http://bluetack.co.uk>`__ and wanna use them.

But pure iptables import sucks. iptables actually is a pretty dumb tool for shiny
netfilter and it sucks back and forth if you have a lot of rules (linear complexity
is WTF in 2014, right?). You googled and found amazing `ipset <http://ipset.netfilter.org/>`__
tool which integrates with iptables perfectly. Lovely. Let's use it.

So this tool just converts gzipped P2P lists into something you can give to
ipset to restore, right? This is a missing tool and you definitely want it.

Why not to use PeerGuardian etc?
--------------------------------

Good question. Actually they are pretty heavyweight and do almost nothing. It is just a
firewall after firewall you already have installed. Look, basically combination of iptables,
ipset and iblocklist2ipset with cron gives you the same features.

Moreover, I want to setup it once and do not worry about anything else. PeerGuardian is
great if you are running this tool on desktop but not on a remote machine. Basically it looks
as excess.

Examples
--------

Well, to give you a feel of a tool, let's just execute it as is:

::

    $ iblocklist2ipset -h
    Small utility to convert p2p format of IP Blocklists to IPSet format.

    Usage:
      iblocklist2ipset generate [options] BLOCKLIST_URL...
      iblocklist2ipset example_restore_ipset_job [options] IPTABLES_NAME IPSET_PATH
      iblocklist2ipset example_update_ipset_job [options] IPSET_PATH BLOCKLIST_URL...
      iblocklist2ipset -h | --help
      iblocklist2ipset --version

    Options:
      -h --help                         Shows this screen.
      --version                         Shows version and exits.
      -i IPSET_NAME --ipset=IPSET_NAME  The name of IPSet set [default: blocklist]

    To get IP blocklists please visit https://www.iblocklist.com/

So as you can see, usage is pretty straightforward. You can give it multiple blocklist
URLs and it will generate you correct file you can restore with ``ipset restore``. Let's do
it with *hijacked* list:

::

    $ iblocklist2ipset generate \
        "http://list.iblocklist.com/?list=usrcshglbiilevmyfhse&fileformat=p2p&archiveformat=gz" \
        > ipset_to_restore
    $ head ipset_to_restore
    create blocklist hash:net family inet hashsize 512 maxelem 536
    add blocklist 81.22.152.0/23
    add blocklist 91.220.163.0/24
    add blocklist 206.209.80.0/20
    add blocklist 204.187.254.0/24
    add blocklist 103.12.216.0/22
    add blocklist 193.0.146.0/23
    add blocklist 208.90.0.0/21
    add blocklist 110.232.160.0/20
    add blocklist 91.213.148.0/24

Quite nice, isn't it? It calculated proper sizes for our list also. Now you can just import it

::

    $ sudo ipset -f ipset_to_restore

And you are safe.

Not really, you need to setup iptables etc to get it work. No problems, if you are using the same
configuration all the times, you can use ``example_restore_ipset_job`` and ``example_update_ipset_job``
commands to get some examples of the usage.

Real world example
------------------

I have my Raspberry Pi running some mission critical software (BTSync for example) and I want to use
`*hijacked* list from IBlockList.com <https://www.iblocklist.com/list.php?list=usrcshglbiilevmyfhse>`__.

I have a Raspbian up to date and now I want to use this shiny tool. First, let's install it.

::

    $ sudo pip install iblocklist2ipset
    $ sudo apt-get install -y ipset

(ipset is not bundled by default so install it before).

I want to store an ipset blocklist into ``/etc/ipset.rules``.

::

    $ iblocklist2ipset example_restore_ipset_job \
        -i hijacked blocklist \
        /etc/ipset.rules \
        > ~/scripts/ipset_restore.sh
    $ chmod +x ~/scripts/ipset_restore.sh

Now we created shell scripts. On execution it will restore iptables and ipset configuration. Please
be noticed that ``iblocklist2ipset`` understands virtualenv usage and script is generated with this
knowledge also.

::

    $ iblocklist2ipset example_update_ipset_job \
        -i hijacked \
        /etc/ipset.rules "http://list.iblocklist.com/?list=usrcshglbiilevmyfhse&fileformat=p2p&archiveformat=gz" \
        > ~/scripts/ipset_update.sh
    $ chmod +x ~/scripts/ipset_update.sh

Lovely. Now we have a script to update. Let's update crontab then

::

    @reboot   /home/user/scripts/ipset_restore.sh
    @midnight /home/user/scripts/ipset_update.sh

Why not to store this stuff into iptables permanently? Well this is mostly because of
ipset configuration. It loses it on reboot and it is not really trivial to restore it.

Probably one day I will do it but right now it has to be like this. At least it works
for me.

Cheers.

.. |Build Status| image:: https://travis-ci.org/9seconds/iblocklist2ipset.svg?branch=master
    :target: https://travis-ci.org/9seconds/iblocklist2ipset

.. |Coverage Status| image:: https://coveralls.io/repos/9seconds/iblocklist2ipset/badge.png?branch=master
    :target: https://coveralls.io/r/9seconds/iblocklist2ipset?branch=master

.. |Health Status| image:: https://landscape.io/github/9seconds/iblocklist2ipset/master/landscape.png
   :target: https://landscape.io/github/9seconds/iblocklist2ipset/master
   :alt: Code Health