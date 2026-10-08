How to create a local mirror of the latest update for Red Hat Enterprise Linux 8 and above without using Satellite server?
 Solution Verified - Updated October 1 2026 at 4:49 PM - English 
Environment
Red Hat Enterprise Linux 8
Red Hat Enterprise Linux 9
Red Hat Enterprise Linux 10
reposync
Issue
What is reposync utility and how to use it?
How to create a local mirror of the latest update for Red Hat Enterprise Linux 8 and above without using Satellite server?
Need to download all packages/rpms from specific channel locally.
How to make a local repository?
Resolution
For RHEL 5, 6 and 7 systems refer How to create a local mirror of the latest update for Red Hat Enterprise Linux 5, 6 and 7 without using Satellite server?

Syncing the latest content
This will sync the latest content available to your system. If you're system is release locked via subscription-manager release, or by /etc/yum/vars/releasever, you will only get the latest content from the releasever specified.
Run reposync command as below to download all packages from the mentioned repoid :

Raw
# reposync -p <download-path> --download-metadata --repoid=<the_repo>

For example:
# reposync -p /var/www/html --download-metadata --repoid=rhel-8-for-x86_64-appstream-rpms
# reposync -p /var/www/html --download-metadata --repoid=rhel-8-for-x86_64-baseos-rpms
Clients can be configured to access this repository with How to create a repo file

By using the reposync -n option, you can collect only the latest packages. This helps save storage space.
Refer to: The reposync process is taking too long to download the packages

Important Note:

createrepo is not required for RHEL 8 and above. reposync will download everything including the
repodata. Any createrepo_c version prior to 0.16.2-1.el8 is not capable of handling module information and
hence tends to remove the module data if run on the RHEL 8 system. If you have the older version and have run
createrepo, check How to add the modules information after cloning the RHEL8 repository.

Ensure to apply the option --download-metadata to pull the metadata.

To sync a specific minor release
Proceed Only if systems are required to be set on specific minor release as 8.4 or 8.6.
For systems registered to the CDN or Red Hat Satellite you must release lock the system with subscription manager

Raw
# subscription-manager release --set=8.4 && rm -rf /var/cache/dnf
At this point your system will only have access to content released for RHEL 8.0- 8.4. If you are syncing multiple minor releases, you must keep these separate from each other. For example to sync both 8.4 and 8.5:

Raw
# subscription-manager release --set=8.4 && rm -rf /var/cache/dnf 
# reposync -p /var/www/html/8.4 --download-metadata --repoid=<repo id> 
# subscription-manager release --set=8.5 && rm -rf /var/cache/dnf 
# reposync -p /var/www/html/8.5 --download-metadata --repoid=<repo id>
Clients can be configured to access this repository with How to create a repo file

How to host a repository using http/https/ftp/nfs ?
Notes:

The -n option can be used to download only the newest version of packages instead of every version of every package.
The --delete option can be used to remove any packages that are not part of the current sync. (Such as older packages when -n downloads a new version)
You will need a system for each major release you are syncing. RHEL 8 can not access RHEL 9 content and vice versa.
On RHEL 8, ensure you have yum-utils-4.0.8-3.el8.noarch or higher installed so reposync correctly downloads all the packages.
RHSA-2019:3583
reposync utility can only mirror repositories which the system is entitled to.
If there are any issues after following above steps, open a Red Hat Technical Support Case and share below details.

Output of the following command :
Raw
# tree /directory_path_of_the_repository
Generate and provide SOS report from the Repo Server and Client.
Root Cause
Red Hat provides a utility called reposync which can be used to download the packages from the CDN. In order to download all packages from a specific channel, the system should be subscribed to that channel. If the system is not subscribed to the required channel then reposync will not be able to download and sync those packages on local system.