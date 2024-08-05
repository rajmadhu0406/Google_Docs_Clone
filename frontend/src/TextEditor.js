import React, { useState, useCallback, useEffect } from 'react'
import Quill from "quill"
import "quill/dist/quill.snow.css"
import "./TextEditor.css"
import { useParams } from 'react-router-dom'


const TextEditor = () => {

    const SAVE_INTERVAL_MS = 2000;

    const [websocket, setWebsocket] = useState(null);
    const [quill, setQuill] = useState();
    const { docId: document_id } = useParams()
    console.log(document_id)



    //useEffect to make sure that the connection is established only once and the return function
    //handles the what to do in case of reload and when rendering is done again
    useEffect(() => {

        const ws = new WebSocket('ws://localhost:8000/api/socket/ws/' + document_id);
        setWebsocket(ws);

        return () => {
            if (ws) {
                ws.close();
            }
        }

    }, [])

    //get-document from database when we load the web page first time
    useEffect(() => {

        if (websocket == null || quill == null) return

        // Function to send a message after ensuring the connection is open
        const sendMessage = (message) => {
            if (websocket.readyState === WebSocket.OPEN) {
                websocket.send(JSON.stringify(message));
            } else {
                console.warn("WebSocket not open. Ready state:", websocket.readyState);
            }
        };

        // Handle WebSocket open event
        const handleOpen = () => {
            // Send message when the connection is open
            const message = {
                key: 'get-document',
                value: document_id
            };
            sendMessage(message);
        };

        // Handle WebSocket open and error events
        websocket.onopen = handleOpen;
        websocket.onerror = (error) => {
            console.error("WebSocket error:", error);
        };

        // Cleanup function to close the WebSocket connection
        return () => {

        };

    }, [websocket, quill, document_id])

    //useEffect for executing function when text changes in quill and for saving the changes in Database
    useEffect(() => {

        if (WebSocket == null || quill == null) return

        const handler = (delta, oldDelta, source) => {
            //make sure that the changes are done by the user and not by quill or the server
            if (source !== 'user') return

            //send changes to server
            if (websocket) {
                // Convert the delta object to a JSON string
                const deltaJson = JSON.stringify(delta);
                const message = {
                    key: 'changes-received',
                    value: deltaJson
                };
                websocket.send(JSON.stringify(message))
            }
        }

        //run handler function on text change
        quill.on('text-change', handler);

        const interval = setInterval(() => {
            if (websocket && ws.readyState === WebSocket.OPEN) {
                // Convert the delta object to a JSON string
                const message = {
                    key: 'save-changes',
                    value: JSON.stringify(quill.getContents())
                };

                console.log("save changes request sent to server with data : ", message);
                websocket.send(JSON.stringify(message))
            }
        }, SAVE_INTERVAL_MS)

        //runs when the component is unmounted
        return () => {
            quill.off('text-change', handler)
            clearInterval(interval);
        }


    }, [websocket, quill])


    //for handling messages received from server like broadcasted chages, new document
    useEffect(() => {

        if (WebSocket == null || quill == null) return

        const handler = (delta) => {
            quill.updateContents(delta);
        }

        if (websocket) {
            //update the document on text change by otheer user by calling handler when we receive delta from server
            websocket.onmessage = (event) => {
                const message = event.data;
                console.log("Message received from server:", message);

                const parsedMessage = JSON.parse(message);

                if (parsedMessage.key === 'update-document' && parsedMessage.value != null) {
                    try {
                        handler(JSON.parse(parsedMessage.value));
                    } catch (e) {
                        console.error("Error parsing message:", e);
                    }
                }

                if (parsedMessage.key === 'db-document') {

                    if (parsedMessage.value != null) {
                        try {
                            const doc_text = JSON.parse(parsedMessage.value).Data;
                            console.log("doc texxt : ", doc_text);
                            if(doc_text){
                                const deltaJsonObject = JSON.parse(doc_text);
                                console.log("deltaJsonObject texxt : ", deltaJsonObject);
                                quill.setContents(deltaJsonObject);
                            }
                            else{
                                quill.setText("");
                            }
                            quill.enable();
                        } catch (e) {
                            console.error("Error parsing message:", e);
                        }
                    }
                    else {
                        quill.setContents("");
                        quill.enable();
                    }

                }
            }
        }


        //runs when the component is unmounted
        return () => {
            // if (websocket)  websocket.close();
        };


    }, [websocket, quill])



    //CONFIGURE THE TOOLBAR OPTIONHS 
    const TOOLBAR_OPTIONS = [
        [{ header: [1, 2, 3, 4, 5, 6, false] }],
        [{ font: [] }],
        [{ list: "ordered" }, { list: "bullet" }],
        ["bold", "italic", "underline"],
        [{ color: [] }, { background: [] }],
        [{ script: "sub" }, { script: "super" }],
        [{ align: [] }],
        ["image", "blockquote", "code-block"],
        ["clean"],
    ]

    // The useCallback function is called from the div with class=container and that div is passed to the function as argument
    //this is done so that the function does not duplicate editors copies when we save some changes.
    const containerRef = useCallback((containerDiv) => {

        if (containerDiv == null) return

        containerDiv.innerHTML = "";
        const editor = document.createElement('div');
        containerDiv.append(editor);

        // Initialize Quill editor
        const q = new Quill(editor, {
            theme: 'snow',
            modules: { toolbar: TOOLBAR_OPTIONS },
        });

        q.disable();
        q.setText('Loading...');
        setQuill(q)

        return () => {
            containerRef.innerHTML = "";
        }

    }, [])


    return (
        <div className="container" ref={containerRef} ></div>
    )
}

export default TextEditor