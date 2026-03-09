"use client";

import {
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ReferenceLine,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

interface ScoreChartProps {
  /** Label of the selected filière (shown in the chart title) */
  filiereName: string;
  /** The four yearly scores */
  score_2022: number | null;
  score_2023: number | null;
  score_2024: number | null;
  score_2025: number | null;
  /** The student's own score to compare against the trend */
  studentScore?: number | null;
}

const YEAR_COLORS = {
  historical: "#6366f1", // indigo
  prediction: "#f59e0b", // amber – 2025 is the prediction
  student: "#ef4444", // red reference line
};

export default function ScoreChart({
  filiereName,
  score_2022,
  score_2023,
  score_2024,
  score_2025,
  studentScore,
}: ScoreChartProps) {
  // Build chart data — omit years with null scores
  const data = [
    { year: "2022", score: score_2022, predicted: false },
    { year: "2023", score: score_2023, predicted: false },
    { year: "2024", score: score_2024, predicted: false },
    { year: "2025", score: score_2025, predicted: true },
  ].filter((d) => d.score !== null);

  const scores = data.map((d) => d.score as number);
  const minY = Math.max(0, Math.floor(Math.min(...scores) - 5));
  const maxY = Math.ceil(Math.max(...scores) + 5);

  /** Custom dot: amber for 2025 prediction, indigo for historical */
  const renderDot = (props: { cx: number; cy: number; payload: { predicted: boolean } }) => {
    const color = props.payload.predicted ? YEAR_COLORS.prediction : YEAR_COLORS.historical;
    return (
      <circle
        key={`dot-${props.cx}-${props.cy}`}
        cx={props.cx}
        cy={props.cy}
        r={5}
        fill={color}
        stroke="#fff"
        strokeWidth={2}
      />
    );
  };

  return (
    <div className="w-full rounded-2xl bg-white p-6 shadow-md">
      <h2 className="mb-1 text-lg font-semibold text-gray-800">
        Évolution des scores d'admission
      </h2>
      <p className="mb-4 text-sm text-gray-500">{filiereName}</p>

      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data} margin={{ top: 10, right: 20, left: 0, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
          <XAxis dataKey="year" tick={{ fontSize: 13 }} />
          <YAxis domain={[minY, maxY]} tick={{ fontSize: 13 }} />
          <Tooltip
            formatter={(value: number) => [`${value.toFixed(4)}`, "Score min."]}
            labelFormatter={(label) =>
              label === "2025" ? `${label} (prédiction)` : label
            }
          />
          <Legend
            formatter={(value) =>
              value === "score" ? "Score minimum d'admission" : value
            }
          />

          {/* Student score reference line */}
          {studentScore != null && (
            <ReferenceLine
              y={studentScore}
              stroke={YEAR_COLORS.student}
              strokeDasharray="6 3"
              label={{
                value: `Votre score: ${studentScore}`,
                fill: YEAR_COLORS.student,
                fontSize: 12,
                position: "insideTopRight",
              }}
            />
          )}

          <Line
            type="monotone"
            dataKey="score"
            stroke={YEAR_COLORS.historical}
            strokeWidth={2.5}
            dot={renderDot as never}
            activeDot={{ r: 7 }}
          />
        </LineChart>
      </ResponsiveContainer>

      {/* Admission verdict */}
      {studentScore != null && score_2025 != null && (
        <div
          className={`mt-4 rounded-lg px-4 py-3 text-sm font-medium ${
            studentScore >= score_2025
              ? "bg-green-50 text-green-700"
              : "bg-red-50 text-red-700"
          }`}
        >
          {studentScore >= score_2025 ? (
            <>
              ✅ Votre score (<strong>{studentScore}</strong>) est{" "}
              <strong>suffisant</strong> pour la tendance 2025 ({score_2025.toFixed(4)}).
            </>
          ) : (
            <>
              ❌ Votre score (<strong>{studentScore}</strong>) est{" "}
              <strong>insuffisant</strong>. Seuil estimé 2025 : {score_2025.toFixed(4)}.
            </>
          )}
        </div>
      )}
    </div>
  );
}
