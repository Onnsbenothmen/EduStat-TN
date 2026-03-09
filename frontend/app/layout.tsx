import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "EduStat-TN",
  description: "Plateforme BI d'orientation universitaire en Tunisie",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="fr">
      <body>{children}</body>
    </html>
  );
}
