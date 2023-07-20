import { BrowserRouter, Routes, Route } from 'react-router-dom';
import MainPage from './MainPage';
import Nav from './Nav';

function App() {
  return (
    <BrowserRouter>
      <Nav />
      <div className="container">
        <Routes>
          <Route path="/" element={<MainPage />} />
          <Route path="shoes" element={<MainPage />} />
            <Route path="new" element={<ShoeForm />} />
            <Route path="details" element={<ShoeDetails />} />
          </Route>

        </Routes>
      </div>
    </BrowserRouter>
  );
}


export default App;
