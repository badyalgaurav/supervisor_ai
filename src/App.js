import React, { useEffect, useRef, useState } from 'react';
import CameraStreaming from './components/CameraStreaming'
import './App.css';
import CameraStream from './components/CameraStreaming';
import PolygonCameraStream from './components/PolygonOverImage';
import DrawPolygons from './components/DrawPolygons';
//reference :-->https://chat.openai.com/c/b43a9db9-14c2-4187-9435-eb8460336b99
function App() {
    //const cams = ["frame", "frame2"];
    //const [imageSrc, setImageSrc] = useState('');
    //let sockets=[]
   

    //    useEffect(() => {
    //        const socket = new WebSocket(`ws://localhost:8000/ws/${0}`);

    //        socket.binaryType = 'arraybuffer';

    //        socket.onmessage = function (event) {
    //            const imageUrl = URL.createObjectURL(new Blob([event.data], { type: 'image/jpeg' }));
    //            setImageSrc(imageUrl);
    //        };

    //        return () => {
    //            socket.close();
    //        };
    //    }, [0]);
       
    const [points, setPoint] = useState();

    const onChange = (data) => {
        setPoint(data);
        console.log(points);
    };
    return (
        <div className="App">
            <header className="App-header">
                <h1>Live Video Streaming</h1>
                {/*<PolygonCameraStream cameraId={0} />*/}
                {/*<DrawCanvas initialData={points} onChange={onChange} />*/}
                {/*<img src={imageSrc} alt={`Camera ${0}`} style={{ width:"100%" }} />*/}
                {/*<img src={imageSrc} alt={`Camera ${0}`} />*/}
                {/*<img src={imageSrc} alt={`Camera ${0}`} />*/}

                <DrawPolygons cameraId={0}></DrawPolygons>
               
            </header>
        </div>
    );
}

export default App;
