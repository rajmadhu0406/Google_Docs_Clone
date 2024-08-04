import React, { useCallback} from 'react'
import Quill from "quill"
import "quill/dist/quill.snow.css"
import "./TextEditor.css"

const TextEditor = () => {


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


    // The useCallback function is called from the div with id=container and that div is passed to the function as argument
    //this is done so that the function does not duplicate editors copies when we save some changes.
    const containerRef = useCallback((containerDiv) => {

        if(containerDiv == null) return
        
        containerDiv.innerHTML = "";
        const editor = document.createElement('div');
        containerDiv.append(editor);

        // Initialize Quill editor
        new Quill(editor, {
            theme: 'snow',
            modules: { toolbar: TOOLBAR_OPTIONS },
        });

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