# clustrun

## Example command template

```
docker run --rm  -v /trials/TRIAL/scans/{0}:/data image_name snakemake
```

## Example setup file

```
docker pull image_name
```

## Example tasks file

```
uk/01/001
uk/02/001
de/01/001
de/01/002
```

## Example invocation

```
clustrun -h hosts -c cmd_tplt -s setup -t tasks
```
