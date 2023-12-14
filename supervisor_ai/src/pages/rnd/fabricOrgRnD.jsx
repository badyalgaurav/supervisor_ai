import React, { useEffect, useState, useRef } from 'react';
import { fabric } from 'fabric';
//refernece :--> https://www.npmjs.com/package/fabric

fabric.Object.prototype.noScaleCache = false;
let line, isDown;
let prevCords;
let vertices = [];
let polygon;
let polyNo = 0;


const FabricOrg = () => {
    const fabricRef = React.useRef(null);
    const loadObjects = () => {
        let defaultObjects = localStorage.getItem("defaultObject") ? JSON.parse(localStorage.getItem('defaultObject')) :[
            {
                "type": "polygon",
                "version": "5.3.0",
                "originX": "left",
                "originY": "top",
                "left": 321,
                "top": 224.2,
                "width": 288,
                "height": 188,
                "fill": "transparent",
                "stroke": "white",
                "strokeWidth": 2,
                "strokeDashArray": null,
                "strokeLineCap": "butt",
                "strokeDashOffset": 0,
                "strokeLineJoin": "miter",
                "strokeUniform": true,
                "strokeMiterLimit": 4,
                "scaleX": 1,
                "scaleY": 1,
                "angle": 0,
                "flipX": false,
                "flipY": false,
                "opacity": 1,
                "shadow": null,
                "visible": true,
                "backgroundColor": "",
                "fillRule": "nonzero",
                "paintFirst": "fill",
                "globalCompositeOperation": "source-over",
                "skewX": 0,
                "skewY": 0,
                "points": [
                    {
                        "x": 15,
                        "y": 61.203125
                    },
                    {
                        "x": 111,
                        "y": 240.203125
                    },
                    {
                        "x": 303,
                        "y": 154.203125
                    },
                    {
                        "x": 236,
                        "y": 52.203125
                    }
                ]
            }
        ]
        fabric.util.enlivenObjects(defaultObjects, (objects) => {
            objects.forEach((obj) => {
                createReadOnlyPolygon(obj.points,obj.left,obj.top,obj.name);
            });
        });
    }
    const initFabric = () => {
        fabricRef.current = new fabric.Canvas('canvas', {
            height: 534,
            width: 812,
            selection:false
        });
        loadObjects();
    };

    const disposeFabric = () => {
        fabricRef.current.dispose();
    };

    useEffect(() => {
        initFabric();
        restrictCrossBoundary();
        return () => {
            disposeFabric();
        };
    }, []);
  function  restrictCrossBoundary(){
        //fabricRef.current.on('object:scaling', function (e) {
        //    console.log("object scaling")

        //    scaling(e);
        //});
        fabricRef.current.on('object:moving', function (e) {
            console.log("object moving")
            movingRotatingWithinBounds(e);
        });
     
        //fabricRef.current.on('object:rotated', function (e) {
        //    console.log("object rotating")
        //    movingRotatingWithinBounds(e);
        //});
 
    }

    let scalingProperties = {
        'left': 0,
        'top': 0,
        'scaleX': 0,
        'scaleY': 0
    }

    function scaling(e) {
        let shape = e.target;
        let maxWidth = shape.canvas.width;
        let maxHeight = shape.canvas.height;

        //left border
        if (shape.left < 0) {
            shape.left = scalingProperties.left;
            shape.scaleX = scalingProperties.scaleX
        } else {
            scalingProperties.left = shape.left;
            scalingProperties.scaleX = shape.scaleX;
        }

        //right border
        if ((scalingProperties.scaleX * shape.width) + shape.left >= maxWidth) {
            shape.scaleX = (maxWidth - scalingProperties.left) / shape.width;
        } else {
            scalingProperties.scaleX = shape.scaleX;
        }

        //top border
        if (shape.top < 0) {
            shape.top = scalingProperties.top;
            shape.scaleY = scalingProperties.scaleY;
        } else {
            scalingProperties.top = shape.top;
            scalingProperties.scaleY = shape.scaleY;
        }

        //bottom border
        if ((scalingProperties.scaleY * shape.height) + shape.top >= maxHeight) {
            shape.scaleY = (maxHeight - scalingProperties.top) / shape.height;
        } else {
            scalingProperties.scaleY = shape.scaleY;
        }
    }

    function movingRotatingWithinBounds(e) {
        const THRESHOLD = 2;
        const obj = e.target;
        // if object is too big ignore
        if (obj.height > obj.canvas.height || obj.width > obj.canvas.width) {
            return;
        }
        obj.setCoords();
        // top-left  corner
        if (obj.getBoundingRect().top < 0 || obj.getBoundingRect().left < 0) {
            obj.top = Math.max(obj.top, obj.top - obj.getBoundingRect().top) + THRESHOLD;
            obj.left = Math.max(obj.left, obj.left - obj.getBoundingRect().left) + THRESHOLD;
        }
        // bot-right corner
        if (obj.getBoundingRect().top + obj.getBoundingRect().height > obj.canvas.height || obj.getBoundingRect().left + obj.getBoundingRect().width > obj.canvas.width) {
            obj.top = Math.min(obj.top, obj.canvas.height - obj.getBoundingRect().height + obj.top - obj.getBoundingRect().top) - THRESHOLD;
            obj.left = Math.min(obj.left, obj.canvas.width - obj.getBoundingRect().width + obj.left - obj.getBoundingRect().left) - THRESHOLD;
        }
        fabricRef.current.requestRenderAll();
    }
    const addPolygon = () => {
        polyNo += 1;
        let name = `poly_${polyNo}`
        drawPolygon(name);
        //const rect = new fabric.Rect({ top: 50, left: 50, stroke: 'red', strokeWidth: 10, width: 100, height: 100, fill: 'rgba(0,0,0,0)', strokeUniform: true });
        //fabricRef.current.add(rect);
    };

    const addRecPolygon = () => {
        let name = `recPoly`
        var allObjects = fabricRef.current.getObjects();
        if (allObjects.filter(e => e.name === name).length > 0) {
            alert("recording polygon already exists");
        }
        else {
            drawPolygon(name);
        }
    };

    //DRAW POLYGON RnD
    const resetCanvas = () => {
        fabricRef.current.off();
        fabricRef.current.clear();
    };
    const deleteActiveObject = () => {
        const activeObject = fabricRef.current.getActiveObject();

        if (activeObject) {
            // Remove the active object from the canvas
            fabricRef.current.remove(activeObject);
            fabricRef.current.discardActiveObject();
            fabricRef.current.renderAll();
        }
    }
    const getPolygonObjects = () => {
        // Assuming fabricRef is a reference to your Fabric.js canvas
        var allObjects = fabricRef.current.getObjects();

        // Filter only the polygon objects
        var polygonObjects = allObjects.filter(function (obj) {
            return obj instanceof fabric.Polygon;
        });

        // Now polygonObjects contains an array of only the polygon objects
        console.log(polygonObjects);
        return polygonObjects;
    }
    const resetVariables = () => {
        line = undefined;
        isDown = undefined;
        prevCords = undefined;
        polygon = undefined;
        vertices = [];
    };
    const resetPolygon = () => {
        polygon = undefined;
    };

    const addVertice = (newPoint) => {
        if (vertices.length > 0) {
            const lastPoint = vertices[vertices.length - 1];
            if (lastPoint.x !== newPoint.x && lastPoint.y !== newPoint.y) {
                vertices.push(newPoint);
            }
        } else {
            vertices.push(newPoint);
        }
    };

    function arePointsClose(checkPoint, threshold) {
        var point2 = checkPoint;
        if (vertices.length > 0) {
            var point1 = vertices[0];
            var distance = Math.sqrt(Math.pow(point2.x - point1.x, 2) + Math.pow(point2.y - point1.y, 2));
            return distance <= threshold;
        }

       
    }
 

    const drawPolygon = (name) => {
        resetVariables();
        //resetCanvas();

        fabricRef.current.on("mouse:down", function (o) {
            isDown = true;
            const pointer = fabricRef.current.getPointer(o.e);

            let points = [pointer.x, pointer.y, pointer.x, pointer.y];

            if (prevCords && prevCords.x2 && prevCords.y2) {
                const prevX = prevCords.x2;
                const prevY = prevCords.y2;
                points = [prevX, prevY, prevX, prevY];
            }

            const newPoint = {
                x: points[0],
                y: points[1]
            };
            if (arePointsClose(newPoint, 5)) {
                console.log('Points are close enough; consider the polygon closed.');
                //verticesList.push(vertices)
                //var polyObjects = getPolygonObjects();
                //deleteAllObjects();
                //for (var i = 0; i < polyObjects.length; i++) {
                //    resetPolygon();
                //    showPolygon(polyObjects[i].points);
                //}
                //resetPolygon();
                createPolygon(vertices, name);
                
                //resetVariables();
          
            } else {
                console.log('Points are not close enough; continue drawing.');
                addVertice(newPoint);

                line = new fabric.Line(points, {
                    strokeWidth: 2,
                    fill: "white",
                    stroke: "white",
                    originX: "center",
                    originY: "center",
                    strokeUniform: true,
                    selectable: false
                });
                fabricRef.current.add(line);
            }
           
        });

        fabricRef.current.on("mouse:move", function (o) {
            if (!isDown) return;
            const pointer = fabricRef.current.getPointer(o.e);
            const coords = {
                x2: pointer.x,
                y2: pointer.y
            };
            line.set(coords);
            prevCords = coords;
            fabricRef.current.renderAll();
        });

        fabricRef.current.on("mouse:up", function (o) {
            const pointer = fabricRef.current.getPointer(o.e);
            const newPoint = {
                x: pointer.x,
                y: pointer.y
            };
            addVertice(newPoint);
        });


    };

    const createReadOnlyPolygon = (vt,left,top, name) => {
        //resetCanvas();
        resetPolygon()
        deleteAllLines();

        if (!polygon) {
            polygon = new fabric.Polygon(vt, {
                fill: "transparent",
                strokeWidth: 2,
                stroke: "white",
                objectCaching: false,
                transparentCorners: false,
                cornerColor: "blue",
                strokeUniform: true,
                left: left,
                top:top
            });
          
        }

        polygon.on("modified", function () {

            var matrix = this.calcTransformMatrix();
            var transformedPoints = this.get("points")
                .map(function (p) {
                    return new fabric.Point(p.x - polygon.minX - polygon.width / 2, p.y - polygon.minY - polygon.height / 2);
                })
                .map(function (p) {
                    return fabric.util.transformPoint(p, matrix);
                });
            var circles = transformedPoints.map(function (p) {
                return new fabric.Circle({
                    left: p.x,
                    top: p.y,
                    radius: 3,
                    fill: "yellow",
                    originX: "center",
                    originY: "center",
                    hasControls: false,
                    hasBorders: false,
                    selectable: false
                });
            });

            //fabricRef.current.clear().add(this).add.apply(this.canvas, circles).setActiveObject(this).renderAll();
            // Render the canvas to reflect the changes
            /*  fabricRef.current.renderAll();*/
        });

        polygon.edit = false;
        polygon.hasBorders = true;
        polygon.cornerColor = "blue";
        polygon.cornerStyle = "rect";
        polygon.controls = fabric.Object.prototype.controls;
        polygon.name = `${name}`;
        fabricRef.current.add(polygon);
        fabricRef.current.renderAll();
        editPolygon();
    };

    const createPolygon = (vt, name) => {
        //resetCanvas();
        deleteAllLines();

        if (!polygon) {
            polygon = new fabric.Polygon(vt, {
                fill: "transparent",
                strokeWidth: 2,
                stroke: "white",
                objectCaching: false,
                transparentCorners: false,
                cornerColor: "blue",
                strokeUniform: true
            });
        }

        polygon.on("modified", function () {
           
            var matrix = this.calcTransformMatrix();
            var transformedPoints = this.get("points")
                .map(function (p) {
                    return new fabric.Point(p.x - polygon.minX - polygon.width / 2, p.y - polygon.minY - polygon.height / 2);
                })
                .map(function (p) {
                    return fabric.util.transformPoint(p, matrix);
                });
            var circles = transformedPoints.map(function (p) {
                return new fabric.Circle({
                    left: p.x,
                    top: p.y,
                    radius: 3,
                    fill: "yellow",
                    originX: "center",
                    originY: "center",
                    hasControls: false,
                    hasBorders: false,
                    selectable: false
                });
            });

            //fabricRef.current.clear().add(this).add.apply(this.canvas, circles).setActiveObject(this).renderAll();
            // Render the canvas to reflect the changes
          /*  fabricRef.current.renderAll();*/
        });

        polygon.edit = false;
        polygon.hasBorders = true;
        polygon.cornerColor = "blue";
        polygon.cornerStyle = "rect";
        polygon.controls = fabric.Object.prototype.controls;
        polygon.name = `${name}`;
        fabricRef.current.add(polygon);
        fabricRef.current.renderAll();
        editPolygon();
    };
    function deleteAllLines() {
        var objects = fabricRef.current.getObjects();

        for (var i = objects.length - 1; i >= 0; i--) {
            if (objects[i] instanceof fabric.Line) {
                fabricRef.current.remove(objects[i]);
            }
        }
        fabricRef.current.off();
        fabricRef.current.discardActiveObject();
        fabricRef.current.renderAll();
    }

    // polygon stuff

    // define a function that can locate the controls.
    // this function will be used both for drawing and for interaction.
    function polygonPositionHandler(dim, finalMatrix, fabricObject) {
        let x = fabricObject.points[this.pointIndex].x - fabricObject.pathOffset.x,
            y = fabricObject.points[this.pointIndex].y - fabricObject.pathOffset.y;
        return fabric.util.transformPoint({
            x: x,
            y: y
        },
            fabric.util.multiplyTransformMatrices(
                fabricObject.canvas.viewportTransform,
                fabricObject.calcTransformMatrix()
            )
        );
    }

    // define a function that will define what the control does
    // this function will be called on every mouse move after a control has been
    // clicked and is being dragged.
    // The function receive as argument the mouse event, the current trasnform object
    // and the current position in canvas coordinate
    // transform.target is a reference to the current object being transformed,
    function actionHandler(eventData, transform, x, y) {
        console.log("test");
        let polygon = transform.target,
            currentControl = polygon.controls[polygon.__corner],
            mouseLocalPosition = polygon.toLocalPoint(
                new fabric.Point(x, y),
                "center",
                "center"
            ),
            polygonBaseSize = polygon._getNonTransformedDimensions(),
            size = polygon._getTransformedDimensions(0, 0),
            finalPointPosition = {
                x: (mouseLocalPosition.x * polygonBaseSize.x) / size.x +
                    polygon.pathOffset.x,
                y: (mouseLocalPosition.y * polygonBaseSize.y) / size.y +
                    polygon.pathOffset.y,
            };
        polygon.points[currentControl.pointIndex] = finalPointPosition;
        return true;
    }

    // define a function that can keep the polygon in the same position when we change its
    // width/height/top/left.
    function anchorWrapper(anchorIndex, fn) {
        return function (eventData, transform, x, y) {
            let fabricObject = transform.target,
                absolutePoint = fabric.util.transformPoint({
                    x: fabricObject.points[anchorIndex].x -
                        fabricObject.pathOffset.x,
                    y: fabricObject.points[anchorIndex].y -
                        fabricObject.pathOffset.y,
                },
                    fabricObject.calcTransformMatrix()
                ),
                actionPerformed = fn(eventData, transform, x, y),
                newDim = fabricObject._setPositionDimensions({}),
                polygonBaseSize = fabricObject._getNonTransformedDimensions(),
                newX =
                    (fabricObject.points[anchorIndex].x -
                        fabricObject.pathOffset.x) /
                    polygonBaseSize.x,
                newY =
                    (fabricObject.points[anchorIndex].y -
                        fabricObject.pathOffset.y) /
                    polygonBaseSize.y;
            fabricObject.setPositionByOrigin(absolutePoint, newX + 0.5, newY + 0.5);
            return actionPerformed;
        };
    }

    function editPolygon() {
       
        fabricRef.current.setActiveObject(polygon);

        polygon.edit = true;
        polygon.hasBorders = false;

        let lastControl = polygon.points.length - 1;
        polygon.cornerStyle = "circle";
        polygon.cornerColor = "yellow";// "rgba(0,0,255,0.5)";
        polygon.controls = polygon.points.reduce(function (acc, point, index) {
            acc["p" + index] = new fabric.Control({
                positionHandler: polygonPositionHandler,
                actionHandler: anchorWrapper(
                    index > 0 ? index - 1 : lastControl,
                    actionHandler
                ),
                actionName: "modifyPolygon",
                pointIndex: index,
            });
            return acc;
        }, {});

        fabricRef.current.requestRenderAll();
        restrictCrossBoundary();
    }
    const handleGetPolygonPoints = () => {
        var canvasObjects = fabricRef.current.getObjects();
        // Customize the serialization of each object
        const serializableObjects = canvasObjects.map(obj => {
            // Include your custom properties here
            return {
                ...obj.toObject(),
                name: obj.name,
                // Add more custom properties as needed
            };
        });
        localStorage.setItem("defaultObject", JSON.stringify(serializableObjects))
        console.log("Serialized objects:", JSON.stringify(serializableObjects));
    }

    const btnStyle = { marginRight: '16px', border: '1px solid #000' };
    return (
        <>
            <button style={btnStyle} onClick={addPolygon}>
                Add Polygon
            </button>
            <button style={btnStyle} onClick={addRecPolygon}>
                Add Rec Polygon
            </button>
            
            <button style={btnStyle} onClick={handleGetPolygonPoints}>
                getPolygonPoints
            </button>
            <button style={btnStyle} onClick={deleteActiveObject}>
                delete
            </button>
            <button style={btnStyle} onClick={resetCanvas}>
                reset
            </button>
            <div style={{ position: 'relative', width: '812px', height: '534px' }}>
                <div style={{ position: 'absolute', top: 0, left: 0 }}>
                    <img
                        src="https://picsum.photos/seed/picsum/200/300"
                        style={{ height: '534px', width: '812px' }}
                    />
                </div>
                <div style={{ position: 'absolute', top: 0, left: 0 }}>
                    <canvas id="canvas" />
                </div>
            </div>
        </>
    );
};

export default FabricOrg;
