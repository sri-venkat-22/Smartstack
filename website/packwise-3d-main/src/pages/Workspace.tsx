// import { useState, useRef, useMemo, useCallback } from 'react';
// import { Canvas, useFrame, useThree, ThreeEvent } from '@react-three/fiber';
// import { OrbitControls, Html, Line, PerspectiveCamera } from '@react-three/drei';
// import * as THREE from 'three';
// import { motion, AnimatePresence } from 'framer-motion';
// import { Navbar } from '@/components/Navbar';
// import { Button } from '@/components/ui/button';
// import { Input } from '@/components/ui/input';
// import { Label } from '@/components/ui/label';
// import { Loader2, Plus, Trash2, Play, RotateCcw, Package, AlertCircle } from 'lucide-react';
// import { useMouse } from '@/hooks/useMouse';

// interface PackedItem {
//   name: string;
//   position: [number, number, number];
//   dimensions: [number, number, number];
// }

// interface ItemInput {
//   id: string;
//   width: number;
//   height: number;
//   depth: number;
// }

// interface BoxProps {
//   position: [number, number, number];
//   dimensions: [number, number, number];
//   name: string;
//   color: string;
//   isHovered: boolean;
//   onClick: () => void;
//   onHover: (hovered: boolean) => void;
// }

// const COLORS = [
//   '#00d4ff', '#8b5cf6', '#10b981', '#f59e0b', '#ec4899',
//   '#06b6d4', '#a855f7', '#22c55e', '#eab308', '#f43f5e'
// ];

// function PackedBox({ position, dimensions, name, color, isHovered, onClick, onHover }: BoxProps) {
//   const meshRef = useRef<THREE.Mesh>(null);
//   const [w, h, d] = dimensions;
//   const [x, y, z] = position;
  
//   // Center the box at its position (position is corner, we need center)
//   const centerPosition: [number, number, number] = [x + w/2, y + h/2, z + d/2];

//   useFrame(() => {
//     if (meshRef.current) {
//       meshRef.current.scale.setScalar(isHovered ? 1.02 : 1);
//     }
//   });

//   return (
//     <group position={centerPosition}>
//       <mesh
//         ref={meshRef}
//         onClick={onClick}
//         onPointerOver={() => onHover(true)}
//         onPointerOut={() => onHover(false)}
//       >
//         <boxGeometry args={[w, h, d]} />
//         <meshStandardMaterial 
//           color={color} 
//           transparent 
//           opacity={isHovered ? 0.9 : 0.75}
//           roughness={0.3}
//           metalness={0.7}
//         />
//       </mesh>
//       <lineSegments>
//         <edgesGeometry args={[new THREE.BoxGeometry(w, h, d)]} />
//         <lineBasicMaterial color={isHovered ? '#ffffff' : color} linewidth={2} />
//       </lineSegments>
      
//       {isHovered && (
//         <Html position={[0, h/2 + 0.5, 0]} center distanceFactor={10}>
//           <div className="glass-panel px-3 py-2 text-xs whitespace-nowrap pointer-events-none">
//             <p className="font-semibold text-foreground">{name}</p>
//             <p className="text-muted-foreground">
//               {w.toFixed(1)} × {h.toFixed(1)} × {d.toFixed(1)}
//             </p>
//             <p className="text-muted-foreground">
//               Pos: ({x.toFixed(1)}, {y.toFixed(1)}, {z.toFixed(1)})
//             </p>
//           </div>
//         </Html>
//       )}
//     </group>
//   );
// }

// function BinWireframe({ dimensions }: { dimensions: [number, number, number] }) {
//   const [w, h, d] = dimensions;
//   const halfW = w / 2;
//   const halfH = h / 2;
//   const halfD = d / 2;

//   const points: [number, number, number][] = [
//     // Bottom face
//     [0, 0, 0], [w, 0, 0],
//     [w, 0, 0], [w, 0, d],
//     [w, 0, d], [0, 0, d],
//     [0, 0, d], [0, 0, 0],
//     // Top face
//     [0, h, 0], [w, h, 0],
//     [w, h, 0], [w, h, d],
//     [w, h, d], [0, h, d],
//     [0, h, d], [0, h, 0],
//     // Vertical edges
//     [0, 0, 0], [0, h, 0],
//     [w, 0, 0], [w, h, 0],
//     [w, 0, d], [w, h, d],
//     [0, 0, d], [0, h, d],
//   ];

//   return (
//     <group position={[0, 0, 0]}>
//       {/* Semi-transparent faces */}
//       <mesh position={[halfW, halfH, halfD]}>
//         <boxGeometry args={[w, h, d]} />
//         <meshStandardMaterial 
//           color="#00d4ff" 
//           transparent 
//           opacity={0.05}
//           side={THREE.DoubleSide}
//         />
//       </mesh>
      
//       {/* Wireframe edges */}
//       {Array.from({ length: 12 }).map((_, i) => (
//         <Line
//           key={i}
//           points={[points[i * 2], points[i * 2 + 1]]}
//           color="#00d4ff"
//           lineWidth={1.5}
//           transparent
//           opacity={0.6}
//         />
//       ))}
      
//       {/* Grid on bottom */}
//       <gridHelper 
//         args={[Math.max(w, d), 10, '#1a3a5c', '#0f2744']} 
//         position={[halfW, 0.001, halfD]} 
//         rotation={[0, 0, 0]}
//       />
//     </group>
//   );
// }

// function CameraController({ binDimensions, focusedItem }: { 
//   binDimensions: [number, number, number];
//   focusedItem: PackedItem | null;
// }) {
//   const { camera } = useThree();
//   const mouse = useMouse();
//   const [w, h, d] = binDimensions;
//   const maxDim = Math.max(w, h, d);
  
//   useFrame(() => {
//     if (focusedItem) {
//       const [x, y, z] = focusedItem.position;
//       const [fw, fh, fd] = focusedItem.dimensions;
//       const targetX = x + fw/2;
//       const targetY = y + fh/2;
//       const targetZ = z + fd/2;
      
//       camera.position.x += (targetX + maxDim * 0.8 - camera.position.x) * 0.05;
//       camera.position.y += (targetY + maxDim * 0.5 - camera.position.y) * 0.05;
//       camera.position.z += (targetZ + maxDim * 0.8 - camera.position.z) * 0.05;
//     } else {
//       // Subtle camera movement based on mouse
//       const targetX = w/2 + mouse.normalizedX * maxDim * 0.2;
//       const targetY = h/2 + maxDim * 0.8 + mouse.normalizedY * maxDim * 0.1;
//       const targetZ = d/2 + maxDim * 1.5;
      
//       camera.position.x += (targetX - camera.position.x) * 0.02;
//       camera.position.y += (targetY - camera.position.y) * 0.02;
//       camera.position.z += (targetZ - camera.position.z) * 0.02;
//     }
    
//     camera.lookAt(w/2, h/2, d/2);
//   });

//   return null;
// }

// function Scene({ 
//   binDimensions, 
//   packedItems, 
//   hoveredItem,
//   focusedItem,
//   setHoveredItem,
//   setFocusedItem 
// }: {
//   binDimensions: [number, number, number];
//   packedItems: PackedItem[];
//   hoveredItem: string | null;
//   focusedItem: PackedItem | null;
//   setHoveredItem: (name: string | null) => void;
//   setFocusedItem: (item: PackedItem | null) => void;
// }) {
//   return (
//     <>
//       <CameraController binDimensions={binDimensions} focusedItem={focusedItem} />
//       <OrbitControls 
//         enableDamping 
//         dampingFactor={0.05}
//         minDistance={3}
//         maxDistance={50}
//       />
      
//       <ambientLight intensity={0.4} />
//       <directionalLight position={[10, 20, 10]} intensity={0.8} castShadow />
//       <pointLight position={[-10, 10, -10]} intensity={0.3} color="#00d4ff" />
      
//       <BinWireframe dimensions={binDimensions} />
      
//       {packedItems.map((item, index) => (
//         <PackedBox
//           key={item.name}
//           position={item.position}
//           dimensions={item.dimensions}
//           name={item.name}
//           color={COLORS[index % COLORS.length]}
//           isHovered={hoveredItem === item.name}
//           onClick={() => setFocusedItem(focusedItem?.name === item.name ? null : item)}
//           onHover={(hovered) => setHoveredItem(hovered ? item.name : null)}
//         />
//       ))}
//     </>
//   );
// }

// export default function Workspace() {
//   const [binWidth, setBinWidth] = useState(10);
//   const [binHeight, setBinHeight] = useState(10);
//   const [binDepth, setBinDepth] = useState(10);
//   const [items, setItems] = useState<ItemInput[]>([
//     { id: '1', width: 3, height: 4, depth: 2 },
//     { id: '2', width: 2, height: 2, depth: 2 },
//     { id: '3', width: 4, height: 3, depth: 3 },
//   ]);
//   const [packedItems, setPackedItems] = useState<PackedItem[]>([]);
//   const [isLoading, setIsLoading] = useState(false);
//   const [error, setError] = useState<string | null>(null);
//   const [hoveredItem, setHoveredItem] = useState<string | null>(null);
//   const [focusedItem, setFocusedItem] = useState<PackedItem | null>(null);

//   const binDimensions: [number, number, number] = [binWidth, binHeight, binDepth];

//   const addItem = () => {
//     setItems([...items, { 
//       id: Date.now().toString(), 
//       width: 2, 
//       height: 2, 
//       depth: 2 
//     }]);
//   };

//   const removeItem = (id: string) => {
//     setItems(items.filter(item => item.id !== id));
//   };

//   const updateItem = (id: string, field: keyof ItemInput, value: number) => {
//     setItems(items.map(item => 
//       item.id === id ? { ...item, [field]: value } : item
//     ));
//   };

//   const generatePacking = async () => {
//     setIsLoading(true);
//     setError(null);
//     setFocusedItem(null);
    
//     try {
//       const response = await fetch('http://localhost:8000/pack', {
//         method: 'POST',
//         headers: { 'Content-Type': 'application/json' },
//         body: JSON.stringify({
//           bin: [binWidth, binHeight, binDepth],
//           items: items.map(item => [item.width, item.height, item.depth])
//         })
//       });

//       if (!response.ok) throw new Error('Packing failed');
      
//       const data = await response.json();
//       setPackedItems(data.packed_items);
//     } catch (err) {
//       // Fallback: simulate packing for demo purposes
//       const simulatedItems: PackedItem[] = [];
//       let currentX = 0;
//       let currentY = 0;
//       let currentZ = 0;
//       let rowMaxHeight = 0;
//       let layerMaxDepth = 0;

//       items.forEach((item, index) => {
//         if (currentX + item.width > binWidth) {
//           currentX = 0;
//           currentY += rowMaxHeight;
//           rowMaxHeight = 0;
//         }
        
//         if (currentY + item.height > binHeight) {
//           currentY = 0;
//           currentZ += layerMaxDepth;
//           layerMaxDepth = 0;
//           rowMaxHeight = 0;
//         }

//         if (currentZ + item.depth <= binDepth) {
//           simulatedItems.push({
//             name: `Item ${index + 1}`,
//             position: [currentX, currentY, currentZ],
//             dimensions: [item.width, item.height, item.depth]
//           });
          
//           currentX += item.width;
//           rowMaxHeight = Math.max(rowMaxHeight, item.height);
//           layerMaxDepth = Math.max(layerMaxDepth, item.depth);
//         }
//       });

//       if (simulatedItems.length < items.length) {
//         setError(`Only ${simulatedItems.length} of ${items.length} items could fit`);
//       }
      
//       setPackedItems(simulatedItems);
//     } finally {
//       setIsLoading(false);
//     }
//   };

//   const reset = () => {
//     setPackedItems([]);
//     setError(null);
//     setFocusedItem(null);
//   };

//   return (
//     <div className="min-h-screen bg-background">
//       <Navbar />
      
//       <div className="flex h-screen pt-20">
//         {/* Control Panel */}
//         <motion.aside
//           initial={{ opacity: 0, x: -20 }}
//           animate={{ opacity: 1, x: 0 }}
//           transition={{ duration: 0.5, delay: 0.2 }}
//           className="w-80 p-6 overflow-y-auto"
//         >
//           <div className="glass-panel p-6 space-y-6">
//             <div>
//               <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
//                 <Package className="w-5 h-5 text-primary" />
//                 Bin Dimensions
//               </h2>
              
//               <div className="grid grid-cols-3 gap-3">
//                 <div>
//                   <Label className="text-xs text-muted-foreground">Width</Label>
//                   <Input
//                     type="number"
//                     value={binWidth}
//                     onChange={(e) => setBinWidth(Number(e.target.value))}
//                     className="input-glass mt-1"
//                     min={1}
//                   />
//                 </div>
//                 <div>
//                   <Label className="text-xs text-muted-foreground">Height</Label>
//                   <Input
//                     type="number"
//                     value={binHeight}
//                     onChange={(e) => setBinHeight(Number(e.target.value))}
//                     className="input-glass mt-1"
//                     min={1}
//                   />
//                 </div>
//                 <div>
//                   <Label className="text-xs text-muted-foreground">Depth</Label>
//                   <Input
//                     type="number"
//                     value={binDepth}
//                     onChange={(e) => setBinDepth(Number(e.target.value))}
//                     className="input-glass mt-1"
//                     min={1}
//                   />
//                 </div>
//               </div>
//             </div>

//             <div className="h-px bg-border" />

//             <div>
//               <div className="flex items-center justify-between mb-4">
//                 <h2 className="text-lg font-semibold">Items ({items.length})</h2>
//                 <Button
//                   variant="ghost"
//                   size="sm"
//                   onClick={addItem}
//                   className="h-8 px-2"
//                 >
//                   <Plus className="w-4 h-4" />
//                 </Button>
//               </div>

//               <div className="space-y-3 max-h-60 overflow-y-auto pr-2">
//                 <AnimatePresence>
//                   {items.map((item, index) => (
//                     <motion.div
//                       key={item.id}
//                       initial={{ opacity: 0, height: 0 }}
//                       animate={{ opacity: 1, height: 'auto' }}
//                       exit={{ opacity: 0, height: 0 }}
//                       className="flex items-center gap-2 p-3 rounded-lg bg-secondary/30"
//                     >
//                       <span 
//                         className="w-3 h-3 rounded-full flex-shrink-0"
//                         style={{ backgroundColor: COLORS[index % COLORS.length] }}
//                       />
//                       <div className="flex-1 grid grid-cols-3 gap-2">
//                         <Input
//                           type="number"
//                           value={item.width}
//                           onChange={(e) => updateItem(item.id, 'width', Number(e.target.value))}
//                           className="input-glass h-8 text-xs"
//                           min={0.1}
//                           step={0.1}
//                         />
//                         <Input
//                           type="number"
//                           value={item.height}
//                           onChange={(e) => updateItem(item.id, 'height', Number(e.target.value))}
//                           className="input-glass h-8 text-xs"
//                           min={0.1}
//                           step={0.1}
//                         />
//                         <Input
//                           type="number"
//                           value={item.depth}
//                           onChange={(e) => updateItem(item.id, 'depth', Number(e.target.value))}
//                           className="input-glass h-8 text-xs"
//                           min={0.1}
//                           step={0.1}
//                         />
//                       </div>
//                       <Button
//                         variant="ghost"
//                         size="icon"
//                         onClick={() => removeItem(item.id)}
//                         className="h-8 w-8 text-muted-foreground hover:text-destructive"
//                       >
//                         <Trash2 className="w-3 h-3" />
//                       </Button>
//                     </motion.div>
//                   ))}
//                 </AnimatePresence>
//               </div>
//             </div>

//             <div className="h-px bg-border" />

//             <div className="space-y-3">
//               <Button
//                 variant="hero"
//                 className="w-full"
//                 onClick={generatePacking}
//                 disabled={isLoading || items.length === 0}
//               >
//                 {isLoading ? (
//                   <>
//                     <Loader2 className="w-4 h-4 animate-spin" />
//                     Packing...
//                   </>
//                 ) : (
//                   <>
//                     <Play className="w-4 h-4" />
//                     Generate Packing
//                   </>
//                 )}
//               </Button>
              
//               {packedItems.length > 0 && (
//                 <Button
//                   variant="glass"
//                   className="w-full"
//                   onClick={reset}
//                 >
//                   <RotateCcw className="w-4 h-4" />
//                   Reset
//                 </Button>
//               )}
//             </div>

//             {error && (
//               <motion.div
//                 initial={{ opacity: 0, y: 10 }}
//                 animate={{ opacity: 1, y: 0 }}
//                 className="p-3 rounded-lg bg-destructive/10 border border-destructive/20 flex items-start gap-2"
//               >
//                 <AlertCircle className="w-4 h-4 text-destructive flex-shrink-0 mt-0.5" />
//                 <p className="text-sm text-destructive">{error}</p>
//               </motion.div>
//             )}

//             {packedItems.length > 0 && (
//               <motion.div
//                 initial={{ opacity: 0 }}
//                 animate={{ opacity: 1 }}
//                 className="p-4 rounded-lg bg-primary/10 border border-primary/20"
//               >
//                 <p className="text-sm font-medium text-primary">
//                   {packedItems.length} items packed successfully
//                 </p>
//                 <p className="text-xs text-muted-foreground mt-1">
//                   Click on items to focus • Drag to rotate view
//                 </p>
//               </motion.div>
//             )}
//           </div>
//         </motion.aside>

//         {/* 3D Canvas */}
//         <div className="flex-1 relative canvas-container">
//           <Canvas
//             dpr={[1, 2]}
//             gl={{ antialias: true, alpha: true }}
//             shadows
//           >
//             <PerspectiveCamera
//               makeDefault
//               position={[binWidth * 1.5, binHeight * 1.2, binDepth * 2]}
//               fov={50}
//             />
//             <Scene
//               binDimensions={binDimensions}
//               packedItems={packedItems}
//               hoveredItem={hoveredItem}
//               focusedItem={focusedItem}
//               setHoveredItem={setHoveredItem}
//               setFocusedItem={setFocusedItem}
//             />
//           </Canvas>

//           {/* Empty state */}
//           {packedItems.length === 0 && !isLoading && (
//             <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
//               <motion.div
//                 initial={{ opacity: 0 }}
//                 animate={{ opacity: 1 }}
//                 transition={{ delay: 0.5 }}
//                 className="text-center"
//               >
//                 <Package className="w-16 h-16 text-muted-foreground/30 mx-auto mb-4" />
//                 <p className="text-lg text-muted-foreground">
//                   Configure items and click "Generate Packing"
//                 </p>
//               </motion.div>
//             </div>
//           )}

//           {/* Loading overlay */}
//           {isLoading && (
//             <div className="absolute inset-0 flex items-center justify-center bg-background/50 backdrop-blur-sm">
//               <motion.div
//                 initial={{ opacity: 0, scale: 0.9 }}
//                 animate={{ opacity: 1, scale: 1 }}
//                 className="glass-panel p-8 text-center"
//               >
//                 <Loader2 className="w-10 h-10 text-primary animate-spin mx-auto mb-4" />
//                 <p className="text-lg font-medium">Computing optimal packing...</p>
//               </motion.div>
//             </div>
//           )}
//         </div>
//       </div>
//     </div>
//   );
// }




import { useState, useRef } from 'react';
import { Canvas, useFrame, useThree } from '@react-three/fiber';
import { OrbitControls, Html, Line, PerspectiveCamera } from '@react-three/drei';
import * as THREE from 'three';
import { motion, AnimatePresence } from 'framer-motion';
import { Navbar } from '@/components/Navbar';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Loader2, Plus, Trash2, Play, RotateCcw, Package, AlertCircle } from 'lucide-react';
import { useMouse } from '@/hooks/useMouse';

interface PackedItem {
  name: string;
  position: [number, number, number];
  dimensions: [number, number, number];
}

interface ItemInput {
  id: string;
  width: number;
  height: number;
  depth: number;
}

const COLORS = [
  '#00d4ff', '#8b5cf6', '#10b981', '#f59e0b', '#ec4899',
  '#06b6d4', '#a855f7', '#22c55e', '#eab308', '#f43f5e'
];

/* -------------------- 3D BOX -------------------- */
function PackedBox({ position, dimensions, name, color, hovered, onHover, onClick }: any) {
  const mesh = useRef<THREE.Mesh>(null);
  const [w, h, d] = dimensions;
  const [x, y, z] = position;

  useFrame(() => {
    if (mesh.current) {
      mesh.current.scale.setScalar(hovered ? 1.03 : 1);
    }
  });

  return (
    <group position={[x + w / 2, y + h / 2, z + d / 2]}>
      <mesh
        ref={mesh}
        onPointerOver={() => onHover(true)}
        onPointerOut={() => onHover(false)}
        onClick={onClick}
      >
        <boxGeometry args={[w, h, d]} />
        <meshStandardMaterial color={color} transparent opacity={0.75} />
      </mesh>

      <lineSegments>
        <edgesGeometry args={[new THREE.BoxGeometry(w, h, d)]} />
        <lineBasicMaterial color={hovered ? '#ffffff' : color} />
      </lineSegments>

      {hovered && (
        <Html distanceFactor={10}>
          <div className="glass-panel px-3 py-2 text-xs">
            <b>{name}</b>
            <div>{w} × {h} × {d}</div>
            <div>({x}, {y}, {z})</div>
          </div>
        </Html>
      )}
    </group>
  );
}

/* -------------------- BIN -------------------- */
function BinWireframe({ dims }: { dims: [number, number, number] }) {
  const [w, h, d] = dims;
  const edges: [number, number, number][] = [
  [0, 0, 0], [w, 0, 0],
  [w, 0, 0], [w, 0, d],
  [w, 0, d], [0, 0, d],
  [0, 0, d], [0, 0, 0],

  [0, h, 0], [w, h, 0],
  [w, h, 0], [w, h, d],
  [w, h, d], [0, h, d],
  [0, h, d], [0, h, 0],

  [0, 0, 0], [0, h, 0],
  [w, 0, 0], [w, h, 0],
  [w, 0, d], [w, h, d],
  [0, 0, d], [0, h, d],
];


  return (
    <>
      <mesh position={[w/2, h/2, d/2]}>
        <boxGeometry args={[w,h,d]} />
        <meshStandardMaterial transparent opacity={0.05} />
      </mesh>

      {Array.from({ length: 12 }).map((_, i) => (
        <Line key={i} points={[edges[i*2], edges[i*2+1]]} color="#00d4ff" />
      ))}
    </>
  );
}

/* -------------------- MAIN -------------------- */
export default function Workspace() {
  const [binWidth, setBinWidth] = useState(10);
  const [binHeight, setBinHeight] = useState(10);
  const [binDepth, setBinDepth] = useState(10);

  const [items, setItems] = useState<ItemInput[]>([
    { id: '1', width: 3, height: 4, depth: 2 },
    { id: '2', width: 2, height: 2, depth: 2 },
  ]);

  const [packedItems, setPackedItems] = useState<PackedItem[]>([]);
  const [hovered, setHovered] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const addItem = () =>
    setItems([...items, { id: Date.now().toString(), width: 2, height: 2, depth: 2 }]);

  const updateItem = (id: string, key: keyof ItemInput, val: number) =>
    setItems(items.map(i => i.id === id ? { ...i, [key]: val } : i));

  const generatePacking = async () => {
    setLoading(true);
    try {
      const res = await fetch('http://localhost:8000/pack', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          bin: [binWidth, binHeight, binDepth],
          items: items.map(i => [i.width, i.height, i.depth])
        })
      });
      const data = await res.json();
      setPackedItems(data.packed_items);
    } catch {
      setPackedItems([]);
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-background">
      <Navbar />

      <div className="flex pt-20 h-screen">
        {/* -------- LEFT PANEL -------- */}
        <aside className="w-80 p-6 space-y-6">
          <div className="glass-panel p-6 space-y-6">

            <div>
              <h2 className="font-semibold mb-3 flex gap-2">
                <Package className="w-5 h-5" /> Bin Dimensions
              </h2>

              <div className="grid grid-cols-3 gap-3">
                {[
                  ['Width', binWidth, setBinWidth],
                  ['Height', binHeight, setBinHeight],
                  ['Depth', binDepth, setBinDepth],
                ].map(([label, value, setter]: any) => (
                  <div key={label}>
                    <Label className="text-xs">{label}</Label>
                    <Input
                      type="number"
                      value={value === 0 ? '' : value}
                      onChange={(e) =>
                        setter(e.target.value === '' ? 0 : Number(e.target.value))
                      }
                      min={1}
                      className="input-glass mt-1"
                    />
                  </div>
                ))}
              </div>
            </div>

            <div className="h-px bg-border" />

            <div>
              <div className="flex justify-between mb-3">
                <h2 className="font-semibold">Items ({items.length})</h2>
                <Button size="sm" variant="ghost" onClick={addItem}>
                  <Plus className="w-4 h-4" />
                </Button>
              </div>

              <div className="space-y-3 max-h-64 overflow-y-auto">
                <AnimatePresence>
                  {items.map((item, i) => (
                    <motion.div
                      key={item.id}
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      exit={{ opacity: 0 }}
                      className="flex items-center gap-2"
                    >
                      <span
                        className="w-3 h-3 rounded-full"
                        style={{ background: COLORS[i % COLORS.length] }}
                      />
                      {(['width','height','depth'] as const).map(k => (
                        <Input
                          key={k}
                          type="number"
                          value={item[k] === 0 ? '' : item[k]}
                          onChange={(e) =>
                            updateItem(item.id, k, e.target.value === '' ? 0 : Number(e.target.value))
                          }
                          className="input-glass h-8 text-xs"
                          min={0.1}
                          step={0.1}
                        />
                      ))}
                      <Button
                        size="icon"
                        variant="ghost"
                        onClick={() => setItems(items.filter(x => x.id !== item.id))}
                      >
                        <Trash2 className="w-3 h-3" />
                      </Button>
                    </motion.div>
                  ))}
                </AnimatePresence>
              </div>
            </div>

            <Button
              variant="hero"
              className="w-full"
              onClick={generatePacking}
              disabled={loading}
            >
              {loading ? <Loader2 className="animate-spin" /> : <Play />}
              Generate Packing
            </Button>
          </div>
        </aside>

        {/* -------- 3D VIEW -------- */}
        <div className="flex-1">
          <Canvas>
            <PerspectiveCamera makeDefault position={[20, 20, 30]} />
            <ambientLight intensity={0.5} />
            <OrbitControls />
            <BinWireframe dims={[binWidth, binHeight, binDepth]} />
            {packedItems.map((item, i) => (
              <PackedBox
                key={item.name}
                {...item}
                color={COLORS[i % COLORS.length]}
                hovered={hovered === item.name}
                onHover={(v: boolean) => setHovered(v ? item.name : null)}
              />
            ))}
          </Canvas>
        </div>
      </div>
    </div>
  );
}
