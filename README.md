# veeam-api

This repository contains a basic Flask application and the related Docker files for returing the Veeam backup results from the database via an HTTP endpoint. Only a subset of the attributes from the `Backup.Model.BackupTaskSessions` table are returned, but you can extend as you see fit.

To get started, clone the repository:

`git clone https://github.com/rsdoherty/veeam-api`

`cd` into the cloned folder, and start the container once you have updated the below in `docker-compose.yml` to connect to the SQL Server Veeam is currently using.

 - `SERVER_ADDRESS`
 - `SERVICE_ACCOUNT`
 - `SERVICE_ACCOUNT_PASSWORD`

`docker-compose -f docker-compose.yml up --build`

You can then browse to http://localhost:8888/backups in your browser, and something similar to the below should be returned, depending on your Veeam environment:

```
➜  ~ curl localhost:8888/backups
[
  {
    "creation_time": "Fri, 27 Mar 2020 00:30:16 GMT",
    "end_time": "Fri, 27 Mar 2020 00:43:44 GMT",
    "id": "1F13A98D-12D9-4D83-B37A-AA8EA59BBC98",
    "object_name": "DESKTOP-TCRE4PR",
    "reason": "",
    "status": 0
  },
  {
    "creation_time": "Fri, 27 Mar 2020 02:00:46 GMT",
    "end_time": "Fri, 27 Mar 2020 02:02:12 GMT",
    "id": "81B39238-83A5-4B37-A5CD-794E010AF7C3",
    "object_name": "000110-kube1",
    "reason": "",
    "status": 0
  },
  {
    "creation_time": "Fri, 27 Mar 2020 02:00:46 GMT",
    "end_time": "Fri, 27 Mar 2020 02:02:40 GMT",
    "id": "259E7D38-32D1-41FE-BAA5-9DA6B178826B",
    "object_name": "000041-rdhost1",
    "reason": "",
    "status": 0
  },
  {
    "creation_time": "Fri, 27 Mar 2020 02:02:02 GMT",
    "end_time": "Fri, 27 Mar 2020 02:04:17 GMT",
    "id": "B752144E-FAF7-4841-9D67-1B70C9E17C5D",
    "object_name": "000083-file1",
    "reason": "",
    "status": 0
  },
  {
    "creation_time": "Fri, 27 Mar 2020 02:03:04 GMT",
    "end_time": "Fri, 27 Mar 2020 02:04:31 GMT",
    "id": "5DE7819D-53AF-436C-B192-45080F2BC2F0",
    "object_name": "000024-wsus",
    "reason": "",
    "status": 0
  },
  {
    "creation_time": "Fri, 27 Mar 2020 02:04:10 GMT",
    "end_time": "Fri, 27 Mar 2020 02:06:04 GMT",
    "id": "BCE45A62-E1F3-4722-9110-74E53976E582",
    "object_name": "000046-ryan",
    "reason": "",
    "status": 0
  },
  {
    "creation_time": "Fri, 27 Mar 2020 02:05:19 GMT",
    "end_time": "Fri, 27 Mar 2020 02:08:21 GMT",
    "id": "B83E1D39-18B3-4030-BADF-3773F538792D",
    "object_name": "000012-db1",
    "reason": "",
    "status": 0
  },
  {
    "creation_time": "Fri, 27 Mar 2020 02:06:43 GMT",
    "end_time": "Fri, 27 Mar 2020 02:07:57 GMT",
    "id": "F999E4F4-5DCB-4874-9814-E371E5AA27C6",
    "object_name": "000111-mc2",
    "reason": "",
    "status": 0
  },
  {
    "creation_time": "Fri, 27 Mar 2020 02:07:49 GMT",
    "end_time": "Fri, 27 Mar 2020 02:09:21 GMT",
    "id": "043B4634-F53F-4A9D-B2CA-B9D7D7F6B9F7",
    "object_name": "000043-dc1",
    "reason": "",
    "status": 0
  },
  {
    "creation_time": "Fri, 27 Mar 2020 02:08:01 GMT",
    "end_time": "Fri, 27 Mar 2020 02:10:18 GMT",
    "id": "1F7C8AE0-8322-4811-98CF-6682A63C452F",
    "object_name": "000090-mc1",
    "reason": "",
    "status": 0
  },
  {
    "creation_time": "Fri, 27 Mar 2020 02:09:15 GMT",
    "end_time": "Fri, 27 Mar 2020 02:10:35 GMT",
    "id": "0E4BB27C-1480-40B3-938C-1B2F020CDE8C",
    "object_name": "000078-docker1",
    "reason": "",
    "status": 0
  },
  {
    "creation_time": "Fri, 27 Mar 2020 02:10:10 GMT",
    "end_time": "Fri, 27 Mar 2020 02:17:58 GMT",
    "id": "37A4A3B6-4148-4C8D-B110-4C682B3D8AF5",
    "object_name": "000023-vcenter",
    "reason": "",
    "status": 0
  },
  {
    "creation_time": "Fri, 27 Mar 2020 02:14:37 GMT",
    "end_time": "Fri, 27 Mar 2020 02:16:08 GMT",
    "id": "FCC24FDB-42AA-45AE-949C-22140687B5A2",
    "object_name": "000013-bast1",
    "reason": "",
    "status": 0
  }
]
```

You can also search for a specific device, by adding the object name to the end of the URL:

```
➜  ~ curl localhost:8888/backups/000110-kube1
[
  {
    "creation_time": "Fri, 27 Mar 2020 02:00:46 GMT",
    "end_time": "Fri, 27 Mar 2020 02:02:12 GMT",
    "id": "81B39238-83A5-4B37-A5CD-794E010AF7C3",
    "object_name": "000110-kube1",
    "reason": "",
    "status": 0
  }
]
```

### Notes

You can also adjust the amount of data returned, but I only need a day for my needs, and didn't want to spend extra time implementing pagination for large results. This can be done by adjusting the `days_to_return` environment variable in `docker-compose.yml`.

We're also using Flask in debug mode, which causes it to auto-reload when it detects a file has changed for faster development.

__Do not enable debug mode in production!__

### Useful Links

* [Flask] - Flask Documentation
* [Docker Compose] - Docker Compose documentation and syntax examples

   [Flask]: <http://flask.palletsprojects.com/en/1.1.x/>
   [Docker Compose]: <https://docs.docker.com/compose/>

