// VideoModal.js
import React from 'react';
import Modal from 'react-modal';

Modal.setAppElement('#root');
const customStyles = {
    content: {
        zIndex: 9999, // Set a high z-index value
    },
};

const VideoModal = ({ isOpen, videoUrl, onRequestClose }) => {
    return (
        <Modal
            isOpen={isOpen}
            onRequestClose={onRequestClose}
            contentLabel="Video Modal"
            style={customStyles} // Apply the custom styles
        >
            <video src={videoUrl} controls autoPlay />
            <button onClick={onRequestClose}>Close</button>
        </Modal>
    );
};

export default VideoModal;
