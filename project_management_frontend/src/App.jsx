import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './components/Login';
import ProtectedRoute from './components/ProtectedRoute';
import ProjectManagement from './components/ProjectManagement';
import ErrorBoundary from './components/ErrorBoundary';

export default function App() {
    return (
        <Router>
            <ErrorBoundary>
                <Routes>
                    <Route path="/login" element={<Login />} />
                    <Route element={<ProtectedRoute />}>
                        <Route path="/" element={<ProjectManagement />} />
                    </Route>
                </Routes>
            </ErrorBoundary>
        </Router>
    );
}
