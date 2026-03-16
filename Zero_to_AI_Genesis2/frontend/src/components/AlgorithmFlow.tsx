'use client';

import { useCallback, useMemo } from 'react';
import {
  ReactFlow,
  Background,
  Controls,
  type Node,
  type Edge,
  Position,
  MarkerType,
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import type { Episode } from '@/data/seasons';

function CustomNode({ data }: { data: { label: string; color: string; nodeType?: string } }) {
  const bgOpacity = data.nodeType === 'input' ? '25' : data.nodeType === 'output' ? '25' : '15';
  const borderOpacity = data.nodeType === 'input' ? '50' : data.nodeType === 'output' ? '50' : '25';

  return (
    <div
      className="px-4 py-3 rounded-xl backdrop-blur-xl text-center min-w-[140px] max-w-[200px] transition-all duration-300 hover:scale-105"
      style={{
        background: `${data.color}${bgOpacity}`,
        border: `1px solid ${data.color}${borderOpacity}`,
        boxShadow: `0 0 20px ${data.color}15`,
      }}
    >
      <span className="text-xs font-medium text-white leading-tight block">
        {data.label}
      </span>
      {data.nodeType === 'input' && (
        <span className="text-[9px] font-accent tracking-wider mt-1 block" style={{ color: data.color }}>INPUT</span>
      )}
      {data.nodeType === 'output' && (
        <span className="text-[9px] font-accent tracking-wider mt-1 block" style={{ color: data.color }}>OUTPUT</span>
      )}
    </div>
  );
}

const nodeTypes = { custom: CustomNode };

export function AlgorithmFlow({ episode, color }: { episode: Episode; color: string }) {
  const { nodes, edges } = useMemo(() => {
    const totalNodes = episode.flowNodes.length;
    const cols = Math.min(totalNodes, 3);
    const rows = Math.ceil(totalNodes / cols);

    const mappedNodes: Node[] = episode.flowNodes.map((node, i) => {
      const row = Math.floor(i / cols);
      const col = i % cols;
      const xOffset = cols > 1 ? (col - (cols - 1) / 2) * 240 : 0;
      return {
        id: node.id,
        type: 'custom',
        position: { x: 300 + xOffset, y: row * 120 },
        data: { label: node.label, color, nodeType: node.type },
        sourcePosition: Position.Bottom,
        targetPosition: Position.Top,
      };
    });

    const mappedEdges: Edge[] = episode.flowEdges.map((edge, i) => ({
      id: `e-${i}`,
      source: edge.source,
      target: edge.target,
      label: edge.label,
      animated: edge.animated ?? true,
      style: { stroke: `${color}60`, strokeWidth: 2 },
      labelStyle: { fill: '#a1a1aa', fontSize: 10, fontFamily: 'Manrope' },
      labelBgStyle: { fill: '#121212', fillOpacity: 0.9 },
      labelBgPadding: [4, 8] as [number, number],
      labelBgBorderRadius: 4,
      markerEnd: { type: MarkerType.ArrowClosed, color: `${color}80`, width: 16, height: 16 },
    }));

    return { nodes: mappedNodes, edges: mappedEdges };
  }, [episode, color]);

  return (
    <div
      data-testid={`algorithm-flow-${episode.id}`}
      className="w-full h-[450px] rounded-xl overflow-hidden border border-white/5"
      style={{ background: '#0a0a0a' }}
    >
      <ReactFlow
        nodes={nodes}
        edges={edges}
        nodeTypes={nodeTypes}
        fitView
        fitViewOptions={{ padding: 0.3 }}
        minZoom={0.5}
        maxZoom={1.5}
        proOptions={{ hideAttribution: true }}
        nodesDraggable={true}
        nodesConnectable={false}
      >
        <Background color="#ffffff08" gap={24} size={1} />
        <Controls
          showInteractive={false}
          style={{ background: '#18181b', borderColor: '#27272a', borderRadius: 8 }}
        />
      </ReactFlow>
    </div>
  );
}
