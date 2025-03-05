import { Navigate } from "react-router-dom";

const PrivateRoute = ({ element }) => {
  const token = localStorage.getItem("access_token"); // LocalStorage'dan token'ı al

  // Eğer token varsa, element'i render et
  if (token) {
    return element;
  }

  // Token yoksa login sayfasına yönlendir
  return <Navigate to="/login" />;
};

export default PrivateRoute;
