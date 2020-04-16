# GitRecycle

This is a project to test the idea of creating a recycle bin for public github projects in order to find projects that are either deleted or went from public to private.

# How it works

Keywords are added and github is searched at interval for new repos. Those repos are archived.

A time limit is set. If the repo is deleted within that time, an alert is generated to review it.

The alerted repo can be dismissed or saved. If dismissed, the archived copy of the repo is deleted.

If the time limit expires, the repo is considered to be stale and is deleted from storage.

