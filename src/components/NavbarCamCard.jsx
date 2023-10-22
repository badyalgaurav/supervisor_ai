import React, { useRef, useState, useEffect, useContext } from "react";
import { useNavigate } from 'react-router-dom';
import { MainContextProvider } from "../utils/MainContextProvider";
const NavbarCamCard = (props) => {
    const navigate = useNavigate();
    const contextData = useContext(MainContextProvider);
    
    const [editBtn, setEditBtn] = useState(false);
    const camNo = props.camNo;
    const data = props.data;

    const handleDrawPolygon = () => {
        contextData.updatePolygonStatusFn(true,camNo)
        setEditBtn(true)
    }
    const handleSavePolygon = () => {
        contextData.updatePolygonStatusFn(false,camNo)
        contextData.savePolygonStatusFn(true, camNo)
        setEditBtn(false)
     
    }
    const handleTaskClick = (cameraId) => {
        // Use the history object to navigate to the desired page
        alert(cameraId)
        const params = {
            cameraId: cameraId
        };
        navigate('/alerteventsreport', { cameraId: params });
    };

    return (<>
        <div className="card navbar_card mt-2" style={{ zIndex: 999 }}>
            <div class="card-header d-flex justify-content-between align-items-center">
                <h6>camera {camNo}</h6>
                <div>
                    {editBtn ? (
                        <button title="edit or add polygon" onClick={handleSavePolygon} type="button" class="btn btn-sm btn-sm-square btn-outline-primary"><i class="fas fa-save"></i></button>
                    ) : (
                        <button title="edit or add polygon" onClick={handleDrawPolygon} type="button" class="btn btn-sm btn-sm-square btn-outline-primary"><i class="fas fa-draw-polygon"></i></button>
                    )}
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