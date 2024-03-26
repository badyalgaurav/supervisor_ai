import React, { useRef, useState, useEffect, useContext } from "react";
import { useNavigate } from 'react-router-dom';
import { MainContextProvider } from "../utils/MainContextProvider";

const NavbarCamCard = (props) => {
    const navigate = useNavigate();
    const contextData = useContext(MainContextProvider);

    //const [editBtn, setEditBtn] = useState(false);
    const camNo = props.camNo;
    const data = props.data;
    const timeData = props.timeData;
    //let sDate = timeData ? timeData[camNo]["startTime"] : "00:00";
    //let eDate = timeData ? timeData[camNo]["endTime"] :"00:00";
    const [startTime, setStartTime] = useState("00:01");
    const [endTime, setEndTime] = useState("23:59");

    const handleDrawPolygon = () => {
        contextData.enableEditingPolygonStatusFn(true, camNo)
        //setEditBtn(true)
    }

    const handleSavePolygon = () => {
       
        contextData.enableEditingPolygonStatusFn(false, camNo)
        contextData.savePolygonStatusFn(true, camNo)
        //setEditBtn(false);
        handleToggle();
    }

    const handleDeleteActiveObject = () => {
        contextData.deleteActivePolygonStatusFn(true, camNo)
    }
    const handleReset = () => {
        contextData.resetStatusFn(true, camNo)
    }
    const addPolygon = () => {
        contextData.addPolygonStatusFn(true, camNo)
    }
    const addRecPolygon = () => {
        contextData.addRecPolygonStatusFn(true, camNo)
    }

    //to show the report page
    const handleTaskClick = (cameraId) => {
        // Use the history object to navigate to the desired page

        const params = {
            cameraId: cameraId
        };
        navigate('/alerteventsreport', { state: params });
    };

    //FOR COLLAPSING ACTION WINDOW
    const [isCollapsed, setIsCollapsed] = useState(true);

    const handleToggle = () => {
        if (isCollapsed) {
            handleDrawPolygon();
        }
        setIsCollapsed(!isCollapsed);
    };

  

    const handleStartTimeChange = (newTime) => {
        setStartTime(newTime.target.value);
    };

    const handleEndTimeChange = (newTime) => {
        setEndTime(newTime.target.value);
    };

    useEffect(() => {
        let sDate = timeData?.[camNo]?.startTime || "00:01";
        let eDate = timeData?.[camNo]?.endTime || "23:59";
        setStartTime(sDate);
        setEndTime(eDate);
    }, [props.timeData])
    return (<>
        <div className="card navbar_card mt-2">
            <div class="card-header d-flex justify-content-between align-items-center">
                <h6>camera {camNo}</h6>
                <div>
                    <button class="btn btn-sm btn-sm-square btn-outline-primary" type="button"
                        data-bs-toggle="collapse" data-bs-target={"#td" + camNo}
                        aria-expanded="false" aria-controls={"td" + camNo}
                        onClick={handleToggle}>{!isCollapsed ? (<i class="fa fa-times" aria-hidden="true"></i>) : (<i class="fa fa-edit" aria-hidden="true"></i>)}

                    </button>
                </div>

            </div>
            <div id={"td" + camNo} style={{ padding: "8px" } } class={`accordion-collapse collapse ${isCollapsed ? '' : 'show'}`}
                aria-labelledby="headingTwo" data-bs-parent="#accordionExample">
                <div class="accordion-head">
                    {/*<button title="edit or add polygon" onClick={handleSavePolygon} type="button" class="btn btn-sm btn-sm-square btn-outline-success m-2"><i class="fas fa-save"></i></button>*/}
              
                        <button title="edit or add polygon" onClick={handleSavePolygon} type="button" class="btn btn-sm btn-sm-square btn-outline-primary"><i class="fas fa-save"></i></button>
                 
                    <button type="button" class="btn btn-sm btn-sm-square btn-outline-success m-2" onClick={addPolygon}><i class="fa fa-plus" aria-hidden="true"></i></button>
                    <button type="button" class="btn btn-sm btn-sm-square btn-outline-success m-2" onClick={addRecPolygon}><i class="fa fas fa-draw-polygon" aria-hidden="true"></i></button>
                    <button type="button" class="btn btn-sm btn-sm-square btn-outline-success m-2" onClick={handleDeleteActiveObject}><i class="fas fa-trash-alt"></i></button>
                    <button type="button" class="btn btn-sm btn-sm-square btn-outline-success m-2" onClick={handleReset}><i class="fa fa-recycle" aria-hidden="true"></i></button>
                    <br></br>
                    <label>Time:</label>
                    <input type="time" id={`startTime_${camNo}`} onChange={handleStartTimeChange}   value={startTime}
                         />
                    <input type="time" id={`endTime_${camNo}`}
                        onChange={handleEndTimeChange}
                        value={endTime}
                      
                    />

                   
                </div>
            </div>
            <div className="card-body navbar-card-body bg-secondary">
                <div class="nav-bar-row  rounded d-flex align-items-center justify-content-between">
                    <i class="fa fa-exclamation-triangle fa-3x text-primary" onClick={() => { handleTaskClick(camNo) }}></i>
                    <div class="ms-3">
                        <h6 class="mb-0 fa-3x"> {data[camNo] ?? 0}</h6>
                    </div>
                </div>
            </div>
        </div>
    </>)
}
export default NavbarCamCard;