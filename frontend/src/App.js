import React from "react";
import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navigation from "./components/Navigation";
import Dashboard from "./components/Dashboard";
import HRServices from "./components/HRServices";
import PolicyCenter from "./components/PolicyCenter";
import ChatAssistant from "./components/ChatAssistant";
import { Toaster } from "./components/ui/toaster";

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <div className="flex">
          {/* Navigation Sidebar */}
          <Navigation />
          
          {/* Main Content Area */}
          <div className="flex-1 ml-64">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/services" element={<HRServices />} />
              <Route path="/policies" element={<PolicyCenter />} />
              <Route path="/chat" element={<ChatAssistant />} />
            </Routes>
          </div>
        </div>
        <Toaster />
      </BrowserRouter>
    </div>
  );
}

export default App;