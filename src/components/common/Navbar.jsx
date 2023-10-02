import React, { useEffect, useState, useContext } from "react";
import NavbarCamCard from "../../components/NavbarCamCard"

const Navbar = (props) => {
    
    return (
        <>
            <div className={`sidebar pb-3 ${props.isOpen ? 'open' : ''}`}>
                <nav class="navbar bg-secondary navbar-dark">
                    <a href="index.html" class="navbar-brand mx-4 mb-3">
                        <h3 class="text-primary"><i class="fa fa-cogs me-2"></i>DarkPan</h3>
                    </a>
                    <div class="navbar-nav w-100">
                        <div class="nav-item dropdown">
                            <div className="">
                                <NavbarCamCard camNo={"1"}></NavbarCamCard>
                            </div>

                            <div className="">
                                <NavbarCamCard camNo={"2"}></NavbarCamCard>
                            </div>
                            <div className="">
                                <NavbarCamCard camNo={"3"}></NavbarCamCard>
                            </div>
                            <div className="">
                                <NavbarCamCard camNo={"4"}></NavbarCamCard>
                            </div>
                        </div>
                    </div>
                </nav>
            </div>
        </>)
};
export default Navbar;