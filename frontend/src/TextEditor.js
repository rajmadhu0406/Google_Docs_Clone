import React, {useState, useCallback, useEffect} from 'react'
import Quill from "quill"
import "quill/dist/quill.snow.css"
import "./TextEditor.css"

const TextEditor = () => {


    const [websocket, setWebsocket] = useState();
    const [quill, setQuill] = useState();
    // const [documentId, setDocumentId] = useState(null);
    // setDocumentId("doc_id_test");

    //useEffect to make sure that the connection is established only once and the return function
    //handles the what to do in case of reload and when rendering is done again
    useEffect(() => {
        
        const ws = new WebSocket('ws://localhost:8000/api/socket/ws/${document_id}');
        setWebsocket(ws);

        return () => {
            if(ws){
                ws.close();
            }
        }

    }, [])

    //useEffect for executing function when text changes in quill
    useEffect(() => {

        if(WebSocket == null || quill == null) return 

        const handler = (delta, oldDelta, source) => {
            //make sure that the changes are done by the user and not by quill or the server
            if(source !== 'user') return
            
            //send changes to server
            if(websocket){
                // Convert the delta object to a JSON string
                const deltaJson = JSON.stringify(delta);
                websocket.send(deltaJson)
            }
        }

        //run handler function on text change
        quill.on('text-change', handler);
        
        //runs when the component is unmounted
        return () => {
            quill.off('text-change', handler )
        }

        
    }, [websocket, quill])


    useEffect(() => {

        if(WebSocket == null || quill == null) return 

        const handler = (delta) => {
            quill.updateContents(delta);
        }

        if(websocket){
            //update the document on text change by otheer user by calling handler when we receive delta from server
            websocket.onmessage = (event) => {
                const message = event.data;
                console.log("Message received from server:", message);

                try {
                    const parsedMessage = JSON.parse(message); // Parse the message if it's in JSON format
                    handler(parsedMessage);
                } catch (e) {
                    console.error("Error parsing message:", e);
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

        if(containerDiv == null) return
        
        containerDiv.innerHTML = "";
        const editor = document.createElement('div');
        containerDiv.append(editor);

        // Initialize Quill editor
        const q = new Quill(editor, {
            theme: 'snow',
            modules: { toolbar: TOOLBAR_OPTIONS },
        });

        setQuill(q)

        return () => {
            containerRef.innerHTML = "";
        }
  
    }, [])


    return (
        <html>
            <body>
                <div className="container" ref={containerRef} ></div>
            </body>
        </html>
        //ddd
    )
}

export default TextEditor