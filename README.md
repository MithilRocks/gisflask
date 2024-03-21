# GIS in Python

A sample project demonstrating a Flask-based RESTful API to serve spatial data from an Open Source Data Hub dataset. This project includes:

A single REST endpoint to return spatial data (e.g., a raster tile)
Example code for data visualization
Unit tests to ensure code correctness
Clear comments to explain the code functionality

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)

## Installation

Build the image and container in detached mode:
```
docker-compose up --build -d
```

The flask app is now running at the following:

```
http://127.0.0.1:5000/tile
```

## Usage

#### Endpoint:

```
  GET /tile
```
This will give us a list of tiles. Clicking on any one of them will lead us to showing that tile.

```
  GET /tile?zoom=10&col=501&row=684
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `zoom` | `int` | **Required**. |
|  `col` | `int` | **Required**       | 
|  `row` | `int` | **Required**       |    

Here we have three values. The zoom, column and row. These values can be used to bring the tile of your choice. A simple map is then plot in the browser.


#### Unit Tests:
You can run the unit tests by the following command. The unit tests are also invoked when the docker image is being created. If the tests fail, the image and container won't be created/updated.

```
python -m unittest tests.py
```
In case you want to run the unittest inside the container:

```
docker exec -it flask python -m unittest tests.py
```


