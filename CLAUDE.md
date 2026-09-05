# monit-rpm

RPM packaging for Monit. CI config is generated from settings.yml by buildstrap;
edit the inputs, not .circleci/config.yml.

Source comes from the upstream Bitbucket release tag. The gittag macro is
updated by builder-scripts/check-new.sh. Bootstrap generates configure and
make builds the manual; keep their BuildRequires when updating the recipe.

## Testing

Fast check (no separate unit suite for this RPM recipe):

```sh
git diff --check
```

Required integration verification runs the real RPM build, rpmlint, and the
spec's check section (binary version and generated man page):

```sh
RPM_REMOTE_HOST=centos@m2.scenery.shop ../builder-scripts/rebuild-remote.sh --dist el9 --ci .
```

Also verify fc44 and sles16 for changes to source preparation or build tools.
Keep generated RPMs and test-results out of commits.
