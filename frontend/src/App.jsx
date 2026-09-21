import { useCallback } from "react";
import {
  ReactFlow,
  Background,
  Controls,
  MiniMap,
  addEdge,
  useNodesState,
  useEdgesState,
} from "@xyflow/react";

import "@xyflow/react/dist/style.css";
import "./App.css";

const initialNodes = [
  {
    id: "ingest",
    position: { x: 80, y: 220 },
    data: {
      label: (
        <div className="pipeline-node">
          <div className="node-icon">⚡</div>
          <div>
            <div className="node-title">INGEST</div>
            <div className="node-tech">Apache Kafka</div>
            <div className="node-status">● Streaming</div>
          </div>
        </div>
      ),
    },
  },

  {
    id: "process",
    position: { x: 400, y: 220 },
    data: {
      label: (
        <div className="pipeline-node">
          <div className="node-icon">⚙</div>
          <div>
            <div className="node-title">PROCESS</div>
            <div className="node-tech">Apache Flink</div>
            <div className="node-status">● Processing</div>
          </div>
        </div>
      ),
    },
  },

  {
    id: "serve",
    position: { x: 720, y: 220 },
    data: {
      label: (
        <div className="pipeline-node">
          <div className="node-icon">◆</div>
          <div>
            <div className="node-title">SERVE</div>
            <div className="node-tech">Apache Iceberg</div>
            <div className="node-status">● Healthy</div>
          </div>
        </div>
      ),
    },
  },
];

const initialEdges = [
  {
    id: "ingest-process",
    source: "ingest",
    target: "process",
    animated: true,
  },
  {
    id: "process-serve",
    source: "process",
    target: "serve",
    animated: true,
  },
];

function App() {
  const [nodes,, onNodesChange] =
    useNodesState(initialNodes);

  const [edges, setEdges, onEdgesChange] =
    useEdgesState(initialEdges);

  const onConnect = useCallback(
    (connection) => {
      setEdges((currentEdges) =>
        addEdge(connection, currentEdges)
      );
    },
    [setEdges]
  );

  return (
    <div className="app">

      {/* HEADER */}

      <header className="header">

        <div className="brand">
          <div className="logo">IS</div>

          <div>
            <h1>IceStream</h1>
            <p>Real-Time Lakehouse Observability</p>
          </div>
        </div>

        <div className="system-status">
          <span className="status-dot"></span>
          ALL SYSTEMS OPERATIONAL
        </div>

      </header>


      {/* MAIN */}

      <main className="main">

        {/* TOP SECTION */}

        <section className="page-heading">

          <div>
            <h2>Pipeline Overview</h2>

            <p>
              Monitor real-time data flow and pipeline health
            </p>
          </div>

          <div className="live-badge">
            LIVE
          </div>

        </section>


        {/* METRICS */}

        <section className="metrics">

          <div className="metric-card">
            <span>EVENTS / SEC</span>
            <strong>1,284</strong>
            <small>Live stream</small>
          </div>

          <div className="metric-card">
            <span>PIPELINE HEALTH</span>
            <strong>99.8%</strong>
            <small>Healthy</small>
          </div>

          <div className="metric-card">
            <span>DATA QUALITY</span>
            <strong>98.7%</strong>
            <small>Current score</small>
          </div>

          <div className="metric-card">
            <span>ACTIVE NODES</span>
            <strong>3 / 3</strong>
            <small>Operational</small>
          </div>

        </section>


        {/* PIPELINE */}

        <section className="pipeline-card">

          <div className="pipeline-header">

            <div>
              <h3>Data Lineage</h3>

              <p>
                Real-time pipeline topology
              </p>
            </div>

            <div className="pipeline-status">
              <span className="status-dot"></span>
              Streaming
            </div>

          </div>


          <div className="flow-container">

            <ReactFlow
              nodes={nodes}
              edges={edges}
              onNodesChange={onNodesChange}
              onEdgesChange={onEdgesChange}
              onConnect={onConnect}
              fitView
            >

              <Background />

              <Controls />

              <MiniMap />

            </ReactFlow>

          </div>

        </section>

      </main>

    </div>
  );
}

export default App;