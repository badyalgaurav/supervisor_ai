// VideoModal.js
import React from 'react';
import Modal from 'react-modal';

Modal.setAppElement('#root');

const VideoModal = ({ isOpen, videoUrl, onRequestClose }) => {
    return (
        <Modal
            isOpen={isOpen}
            onRequestClose={onRequestClose}
            contentLabel="Video Modal"
        >
            <video src={videoUrl} controls autoPlay />
            <button onClick={onRequestClose}>Close</button>
        </Modal>
    );
};

export default VideoModal;
