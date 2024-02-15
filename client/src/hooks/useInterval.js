// https://github.com/craig1123/react-recipes/blob/master/src/useInterval.js

import { useEffect, useRef } from "react";

function useInterval(
  callback,
  delay,
  runOnLoad = false,
  effectDependencies = [],
) {
  const savedCallback = useRef();

  useEffect(() => {
    if (runOnLoad) {
      callback();
    }
  }, [...effectDependencies]);

  useEffect(() => {
    savedCallback.current = callback;
  }, [callback]);

  useEffect(() => {
    if (delay !== null) {
      const id = setInterval(() => savedCallback.current(), delay);
      return () => clearInterval(id);
    }
  }, [delay, ...effectDependencies]);
}

export default useInterval;
