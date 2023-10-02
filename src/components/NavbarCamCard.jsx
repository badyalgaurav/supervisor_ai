import React, { useRef, useState, useEffect, useContext } from "react";
import { MainContextProvider } from "../utils/MainContextProvider";
const NavbarCamCard = (props) => {

    const contextData = useContext(MainContextProvider);
    
    const [editBtn, setEditBtn] = useState(false);
    const camNo = props.camNo;

    const handleDrawPolygon = () => {
        contextData.updatePolygonStatusFn(true,camNo)
        setEditBtn(true)
        alert(camNo);
    }
    const handleSavePolygon = () => {
        contextData.updatePolygonStatusFn(false,camNo)
        setEditBtn(false)
        alert(camNo);
    }

    return (<>
        <div className="card navbar_card mt-2">
            <div class="card-header d-flex justify-content-between align-items-center">
                <h6>camera {camNo}</h6>
                <p>Context State: {contextData.updatePolygonStatus}</p>
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
                    <i class="fa fa-exclamation-triangle fa-3x text-primary"></i>
                    <div class="ms-3">
                        <h6 class="mb-0 fa-3x">1234</h6>
                    </div>
                </div>
                <div class="nav-bar-row  rounded d-flex align-items-center justify-content-between">
                    <i class="fa fa-exclamation-triangle fa-3x text-primary"></i>
                    <div class="ms-3">
                        <h6 class="mb-0 fa-3x">1234</h6>
                    </div>
                </div>
                <div class="nav-bar-row  rounded d-flex align-items-center justify-content-between">
                    <i class="fa fa-exclamation-triangle fa-3x text-primary"></i>
                    <div class="ms-3">
                        <h6 class="mb-0 fa-3x">1234</h6>
                    </div>
                </div>
            </div>
        </div>
    </>)
}
export default NavbarCamCard;