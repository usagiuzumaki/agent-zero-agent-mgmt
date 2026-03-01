"use client";

import BookEditor from "@/components/editor/BookEditor";
import { useParams } from "next/navigation";

export default function BookPage() {
  const params = useParams<{ projectId: string }>();
  return <BookEditor projectId={params.projectId} />;
}
