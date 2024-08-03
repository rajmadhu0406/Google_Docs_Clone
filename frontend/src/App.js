import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import Home from './Home';
import Test from './Test';
import TextEditor from './TextEditor';

function App() {
  return (
    <Router>
      <div className="App">
        {/* Route Configuration */}
        <Routes>
          <Route path="/" element={<Home />} /> {/* Updated route path to '/' */}
          <Route path="/test" element={<Test />} />
          <Route path="/editor" element={<TextEditor />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
