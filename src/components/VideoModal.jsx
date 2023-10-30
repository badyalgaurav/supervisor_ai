// VideoModal.js
import React from 'react';
import Modal from 'react-modal';
import { apiSAIFrameworkAPIPath } from "../config"
Modal.setAppElement('#root');

const VideoModal = ({ isOpen, videoUrl, onRequestClose }) => {
    const f_path = `${apiSAIFrameworkAPIPath}/mongo_op/video/?video_path=${videoUrl}`
    return (
        <Modal
            isOpen={isOpen}
            onRequestClose={onRequestClose}
            style={{
                content: {
                    top: '50%',
                    left: '50%',
                    right: 'auto',
                    bottom: 'auto',
                    transform: 'translate(-50%, -50%)',
                    //margin: 0, // Remove the margin
                    padding:0
                },
            }}
            contentLabel="Video Modal">
            <div className="modal-header">
                <h6 className="align-items-center">Video</h6><button className="close-button" onClick={onRequestClose}>X</button></div>
            <div className="modal-content">
                <video controls width="100%" height="100%">
                    <source src={f_path} type="video/mp4"></source>
                        Your browser does not support the video tag.
                </video>
            </div>
        </Modal>
    );
};

export default VideoModal;
