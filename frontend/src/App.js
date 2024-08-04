import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { v4 as uuidV4 } from "uuid"
import './App.css';
import Home from './Home';
import Test from './Test';
import TextEditor from './TextEditor';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/test" element={<Test />} />
        <Route path="/new" element={<Navigate to={`/editor/${uuidV4()}`} />} />
        <Route path="/editor/:docId" element={<TextEditor />} />
      </Routes>
    </Router>
  );
}


export default App;


// <body>
//   <Router>
//     <div className="App">
//       {/* Route Configuration */}
//       <Routes>
//         <Route path="/" element={<Home />} /> {/* Updated route path to '/' */}
//         <Route path="/test" element={<Test />} />
//         <Route path="/editor" element={<TextEditor />} />
//       </Routes>
//     </div>
//   </Router>
// </body>