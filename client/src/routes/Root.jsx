import { Outlet } from "react-router-dom";

export default function Root() {
  return (
      <div>
        <h1>canihasashowplz</h1>
        <Outlet />
      </div>
  );
}