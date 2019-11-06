# Docker conda-channel

Docker container to create and serve a custom conda channel.

Based on the documentation on [custom channels](http://conda.pydata.org/docs/custom-channels.html)

## Usage

To create a custom channel, first organize all the packages in subdirectories
for the platforms you wish to serve.

```
channel/
  linux-32/
    package-1.0-0.tar.bz
  linux-64/
    package-1.0-0.tar.bz
  osx-64/
    package-1.0-0.tar.bz
  win-64/
    package-1.0-0.tar.bz
  ...
```

Now start the container sharing the `channel` directory as a volume

```
docker run -v $(pwd)/channel:/channel -p 8080:80 -it danielfrg/conda-channel
```

You can now go to: `http://{DOCKER_HOST}:8080` and see the channel repo.

## Common errors

**403 on packages**: This usually means that the container user executing nginx
cannot read the packages.
Make sure all the `tar.bz2` files are readable by all users: `chmod 644 *.tar.bz2`

**noach/repodata.json
have to build this dir first
https://repo.anaconda.com/pkgs/main/noarch/repodata.json

download all bioconda
- https://conda.anaconda.org/bioconda/linux-64
  - https://conda.anaconda.org/bioconda/noarch
  - https://repo.continuum.io/pkgs/main/linux-64
  - https://repo.continuum.io/pkgs/main/noarch
  - https://repo.continuum.io/pkgs/free/linux-64
  - https://repo.continuum.io/pkgs/free/noarch
  - https://repo.continuum.io/pkgs/r/linux-64
  - https://repo.continuum.io/pkgs/r/noarch
  - https://repo.continuum.io/pkgs/pro/linux-64
  - https://repo.continuum.io/pkgs/pro/noarch

