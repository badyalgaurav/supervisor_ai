import React, { useEffect, useState, useRef, useContext } from 'react';
import { fabric } from 'fabric';
import axios from 'axios';
import Swal from "sweetalert2";
import { MainContextProvider } from "../../utils/MainContextProvider";
import { apiSAIFrameworkAPIPath, apiWebSocketPath } from "../../config"
//refernece :--> https://www.npmjs.com/package/fabric

fabric.Object.prototype.noScaleCache = false;
let line, isDown;
let prevCords;
let vertices = [];
let polygon;
let polyNo = 0;

const FabricJSCanvas = (props) => {
    const contextData = useContext(MainContextProvider);

    const cameraId = props.cameraId;
    const canvasId = 'canvas_' + cameraId;

    const [polyEditable, setPolyEditable] = useState(false);
    const fabricRef = React.useRef(null);
    const loadObjects = () => {
        const apiUrl = `${apiSAIFrameworkAPIPath}/mongo_op/get_polygon`; // Replace with your API endpoint URL
        const requestData = {
            // "camera_no": parseInt(cameraId)

        };

        axios.get(apiUrl, {
            params: requestData
        })
            .then((response) => {
                debugger;
                const responseData = response.data.data;
                for (let i = 0; i < responseData.length; i++) {
                    const item = responseData[i];
                    if (parseInt(cameraId) == item.camera_no) {
                        fabric.util.enlivenObjects(item.polyRawInfo, (objects) => {
                            objects.forEach((obj) => {
                                createReadOnlyPolygon(obj);
                            });
                        });
                    }
                    //localStorage.setItem(`polyFor_${item.camera_no}`, JSON.stringify(item.polygonInfo))
                    // Process each item in the response data here
                }
            })
            .catch((error) => {
                // Handle any errors that occurred during the request
                console.error('Error:', error);
            });


    }
    const initFabric = () => {
        fabricRef.current = new fabric.Canvas(canvasId, {
            height: 534,
            width: 812,
            selection: false
        });
        loadObjects();
    };

    const disposeFabric = () => {
        fabricRef.current.dispose();
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

    const addPolygon = () => {
        polyNo += 1;
        let name = `poly_${polyNo}`
        //drawPolygon(name);
        //const rect = new fabric.Rect({ top: 50, left: 50, stroke: 'red', strokeWidth: 10, width: 100, height: 100, fill: 'rgba(0,0,0,0)', strokeUniform: true });
        //fabricRef.current.add(rect);
        var allObjects = fabricRef.current.getObjects();
        if (allObjects.filter(e => e.name.includes("poly_")).length > 0) {
            alert("polygon already exists");
        }
        else {
            drawPolygon(name);
        }
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
                createPolygon(vertices, name);
            } else {
                console.log('Points are not close enough; continue drawing.');
                addVertice(newPoint);

                line = new fabric.Line(points, {
                    strokeWidth: 2,
                    fill: name == "recPoly" ? "white" : "red",
                    stroke: name == "recPoly" ? "white" : "red",
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

    const createReadOnlyPolygon = (obj) => {
        //resetCanvas();
        resetPolygon()
        deleteAllLines();
        // Define points for a simple polygon using pixel values
        //var points = [
        //    { x: 100, y: 100 },   // pixel position for the first point
        //    { x: 200, y: 100 },   // pixel position for the second point
        //    { x: 200, y: 200 },   // pixel position for the third point
        //    { x: 100, y: 200 }    // pixel position for the fourth point
        //];
        polygon = new fabric.Polygon(obj.points, {
            fill: "transparent",
            strokeWidth: 2,
            stroke: obj.stroke,
            objectCaching: false,
            transparentCorners: false,
            cornerColor: "blue",
            strokeUniform: true,
            left: obj.left,
            top: obj.top,
            controls: fabric.Object.prototype.controls,
            name: `${obj.name}`,
            editable: polyEditable,
            selectable: polyEditable,
            evented: polyEditable,
        });
        fabricRef.current.add(polygon);
        fabricRef.current.renderAll();
        editPolygon();
    };

    const createPolygon = (vt, name) => {
        deleteAllLines();
        if (!polygon) {
            polygon = new fabric.Polygon(vt, {
                fill: "transparent",
                strokeWidth: 2,
                stroke: name == "recPoly" ? "white" : "red",
                objectCaching: false,
                transparentCorners: false,
                cornerColor: "blue",
                strokeUniform: true,
                name: name
            });
        }

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
    const handleSavePolygonInfo = () => {
        debugger;
        var startTime = document.getElementById(`startTime_${cameraId}`).value;
        let endTime = document.getElementById(`endTime_${cameraId}`).value;

        var allObjects = fabricRef.current.getObjects();
        // Filter only the polygon objects
        var polygonObjects = allObjects.filter(function (obj) {
            return obj instanceof fabric.Polygon;
        });

        // Customize the serialization of each object
        const serializableObjects = polygonObjects.map(obj => {
            //need to translate the relative points to absolute
            var matrix = obj.calcTransformMatrix();
            var transformedPoints = obj.get("points")
                .map(function (p) {
                    return new fabric.Point(
                        p.x - obj.pathOffset.x,
                        p.y - obj.pathOffset.y);
                })
                .map(function (p) {
                    return fabric.util.transformPoint(p, matrix);
                });

            // Include your custom properties here
            return {
                ...obj.toObject(),
                name: obj.name,
                transformedPoints: transformedPoints
                // Add more custom properties as needed
            };
        });
        localStorage.setItem("defaultObject", JSON.stringify(serializableObjects))
        console.log("Serialized objects:", JSON.stringify(serializableObjects));
        const apiUrl = `${apiSAIFrameworkAPIPath}/mongo_op/upsert_polygon/`;
        const requestData = {
            "camera_no": parseInt(cameraId),
            "polygon_info": JSON.stringify(serializableObjects),
            "start_time": startTime ?? "00:00",
            "end_time": endTime ?? "00:00"
        };

        axios.post(apiUrl, requestData)
            .then((response) => {
                // Handle the successful response here
                console.log('Response data:', response.data);
                showSuccessAlert();
                // to disable editing the polygon after saved
                setPolyEditable(false);
            })
            .catch((error) => {
                // Handle any errors that occurred during the request
                console.error('Error:', error);
            });
    }
    const showSuccessAlert = () => {
        Swal.fire({
            icon: "success",
            title: "Saved!",
            text: "Your changes have been successfully saved.",
        });
    };

    useEffect(() => {

        initFabric();
        restrictCrossBoundary();
        return () => {
            disposeFabric();
        };
    }, [polyEditable]);

    function restrictCrossBoundary() {
        fabricRef.current.on('object:moving', function (e) {
            console.log("object moving")
            movingRotatingWithinBounds(e);
        });
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

    //Context change status
    useEffect(() => {

        // Execute your desired function here
        console.log('Context Data has changed:');
        if (contextData.enableEditingPolygonStatus[parseInt(cameraId) - 1] == true) {
            //canvasRef.current.toggleDraw();
            setPolyEditable(true);
        }
        //if (contextData.enableEditingPolygonStatus[parseInt(cameraId) - 1] == false) {
        //    setPolyEditable(false);
        //    console.log(cameraId)
        //    //handleSavePolygonInfo();


        //}
        if (contextData.savePolygonStatus[parseInt(cameraId) - 1] == true) {


            handleSavePolygonInfo();
            contextData.savePolygonStatusFn(false, cameraId);
            //setTimeout(setPolyEditable(false),1500)

        }
        if (contextData.deleteActivePolygonStatus[parseInt(cameraId) - 1] == true) {
            deleteActiveObject();
            contextData.deleteActivePolygonStatusFn(false, cameraId)
        }
        if (contextData.deleteActivePolygonStatus[parseInt(cameraId) - 1] == true) {
            deleteActiveObject();
            contextData.deleteActivePolygonStatusFn(false, cameraId)
        }
        if (contextData.resetStatus[parseInt(cameraId) - 1] == true) {
            resetCanvas();
            contextData.resetStatusFn(false, cameraId)
        }

        if (contextData.addPolygonStatus[parseInt(cameraId) - 1] == true) {
            addPolygon();
            contextData.addPolygonStatusFn(false, cameraId)
        }
        if (contextData.addRecPolygonStatus[parseInt(cameraId) - 1] == true) {
            addRecPolygon();
            contextData.addRecPolygonStatusFn(false, cameraId)
        }

    }, [contextData]);

    return (<> <canvas id={canvasId} /></>)
};

export default FabricJSCanvas;