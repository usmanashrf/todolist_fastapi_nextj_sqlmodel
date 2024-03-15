import { NextRequest, NextResponse } from "next/server";

export async function GET(request: NextRequest) {
        const res = await fetch("https://hardy-flamingo-concrete.ngrok-free.app/todos");
        return await res.json(); // res.json();
}