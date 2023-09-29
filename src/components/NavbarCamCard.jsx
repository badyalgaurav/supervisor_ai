import React, { useRef, useState, useEffect } from "react";

const NavbarCamCard = () => {
    return (<>
        <div className="card navbar_card mt-2">
            <div class="card-header d-flex justify-content-between align-items-center">
                <h6>cam1</h6>
                <div>
                    <button title="edit or add polygon" type="button" class="btn btn-sm btn-sm-square btn-outline-primary"><i class="fas fa-draw-polygon"></i></button>
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
                {/*<div class="nav-bar-row  rounded d-flex align-items-center justify-content-between">*/}
                {/*    <i class="fa fa-chart-line fa-3x text-primary"></i>*/}
                {/*    <div class="ms-3">*/}
                {/*        <p class="mb-2">Today Sale</p>*/}
                {/*        <h6 class="mb-0">$1234</h6>*/}
                {/*    </div>*/}
                {/*</div>*/}
            </div>
        </div>
    </>)
}
export default NavbarCamCard;