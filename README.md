# GIS in Python

A brief description of your project.

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
http://192.168.207.2:5000
```

## Usage

```
  GET /tile?zoom=10&col=501&row=684
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `zoom` | `int` | **Required**. |
|  `col` | `int` | **Required**       | 
|  `row` | `int` | **Required**       |    

Here we have three values. The zoom, column and row. These values can be used to bring the tile of your choice. A simple map is then plot in the browser.
