import { NextRequest, NextResponse } from "next/server";

export const config = {
  matcher: ["/admin/:path*"],
};

export default function middleware(req: NextRequest) {
  const url = new URL(req.url);

  // Permite sem autenticação em desenvolvimento
  const isDev = process.env.NODE_ENV !== "production";
  if (isDev) return NextResponse.next();

  const authHeader = req.headers.get("authorization") || "";
  const [scheme, encoded] = authHeader.split(" ");

  // Sem credencial → pedir auth
  if (scheme !== "Basic" || !encoded) {
    return new NextResponse("Authentication required", {
      status: 401,
      headers: { "WWW-Authenticate": "Basic realm=\"Protected\"" },
    });
  }

  // Validar credenciais
  const decoded = Buffer.from(encoded, "base64").toString();
  const [user, pass] = decoded.split(":");

  const expectedUser = process.env.BASIC_AUTH_USER || "";
  const expectedPass = process.env.BASIC_AUTH_PASS || "";

  if (!expectedUser || !expectedPass) {
    // Se não configurado em produção, bloqueia por segurança
    return new NextResponse("Server auth not configured", { status: 500 });
  }

  if (user !== expectedUser || pass !== expectedPass) {
    return new NextResponse("Invalid credentials", {
      status: 401,
      headers: { "WWW-Authenticate": "Basic realm=\"Protected\"" },
    });
  }

  return NextResponse.next();
}
