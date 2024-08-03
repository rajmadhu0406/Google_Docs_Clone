import React, { useEffect } from 'react'
import Quill from 'quill'
import "quill/dist/quill.snow.css"

const TextEditor = () => {

    //runs once when the this page gets rendered the first time
    useEffect(() => {
        new Quill('#container', {theme: "snow"})
    }, [])
    

    return (
    <div id="container"></div>
    )
}

export default TextEditor