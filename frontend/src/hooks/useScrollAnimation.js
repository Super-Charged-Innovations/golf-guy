import { useEffect, useRef, useState } from 'react';

export const useScrollAnimation = (options = {}) => {
  const elementRef = useRef(null);
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsVisible(true);
          // Optionally unobserve after triggering
          if (options.once !== false) {
            observer.unobserve(entry.target);
          }
        } else if (options.once === false) {
          setIsVisible(false);
        }
      },
      {
        threshold: options.threshold || 0.1,
        rootMargin: options.rootMargin || '0px',
      }
    );

    const currentElement = elementRef.current;
    if (currentElement) {
      observer.observe(currentElement);
    }

    return () => {
      if (currentElement) {
        observer.unobserve(currentElement);
      }
    };
  }, [options.threshold, options.rootMargin, options.once]);

  return [elementRef, isVisible];
};

// Batch scroll animation for multiple elements
export const useScrollAnimations = (count, options = {}) => {
  const [refs, setRefs] = useState([]);
  const [visibleItems, setVisibleItems] = useState(new Set());

  useEffect(() => {
    // Create refs array
    const newRefs = Array.from({ length: count }, () => useRef(null));
    setRefs(newRefs);
  }, [count]);

  useEffect(() => {
    if (refs.length === 0) return;

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          const index = refs.findIndex(ref => ref.current === entry.target);
          if (index !== -1 && entry.isIntersecting) {
            setVisibleItems(prev => new Set([...prev, index]));
            if (options.once !== false) {
              observer.unobserve(entry.target);
            }
          } else if (options.once === false && !entry.isIntersecting) {
            setVisibleItems(prev => {
              const newSet = new Set(prev);
              newSet.delete(index);
              return newSet;
            });
          }
        });
      },
      {
        threshold: options.threshold || 0.1,
        rootMargin: options.rootMargin || '0px',
      }
    );

    refs.forEach(ref => {
      if (ref.current) {
        observer.observe(ref.current);
      }
    });

    return () => {
      refs.forEach(ref => {
        if (ref.current) {
          observer.unobserve(ref.current);
        }
      });
    };
  }, [refs, options.threshold, options.rootMargin, options.once]);

  return [refs, visibleItems];
};
