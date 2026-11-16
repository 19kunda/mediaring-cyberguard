
export default function Home() {
  return (
    <main className="min-h-screen bg-[#071426] text-white">

      {/* Navigation */}
      <nav className="flex items-center justify-between px-8 py-6 lg:px-16">
        <div>
          <h1 className="text-2xl font-bold tracking-wide">
            MediaRing<span className="text-blue-400"> CyberGuard</span>
          </h1>
          <p className="mt-1 text-xs tracking-widest text-slate-400">
            WEBSITE SECURITY PLATFORM
          </p>
        </div>

        <div className="hidden items-center gap-8 text-sm text-slate-300 md:flex">
          <a href="#features" className="hover:text-blue-400">
            Features
          </a>
          <a href="#about" className="hover:text-blue-400">
            About
          </a>
          <a href="#login" className="rounded-lg border border-blue-400/50 px-5 py-2.5 hover:bg-blue-500/10">
            Customer Login
          </a>
        </div>
      </nav>

      {/* Main content */}
      <section className="mx-auto grid max-w-7xl items-center gap-16 px-8 py-16 lg:grid-cols-2 lg:px-16 lg:py-28">

        {/* Welcome section */}
        <div>
          <div className="mb-8 inline-flex items-center gap-2 rounded-full border border-blue-400/30 bg-blue-400/10 px-4 py-2 text-sm text-blue-300">
            <span className="h-2 w-2 rounded-full bg-blue-400"></span>
            Website security made accessible
          </div>

          <h2 className="max-w-xl text-5xl font-bold leading-tight tracking-tight md:text-6xl">
            Protect your digital presence.
            <span className="mt-2 block text-blue-400">
              Stay one step ahead.
            </span>
          </h2>

          <p className="mt-8 max-w-lg text-lg leading-8 text-slate-400">
            MediaRing CyberGuard is being developed to help businesses
            identify website security concerns, understand potential risks
            and make more informed security decisions.
          </p>

          <div id="features" className="mt-12 grid gap-6 sm:grid-cols-2">
            <div className="rounded-xl border border-white/10 bg-white/[0.04] p-5">
              <div className="mb-3 text-2xl text-blue-400">01</div>
              <h3 className="font-semibold">Website Security</h3>
              <p className="mt-2 text-sm leading-6 text-slate-400">
                Identify potential website security concerns.
              </p>
            </div>

            <div className="rounded-xl border border-white/10 bg-white/[0.04] p-5">
              <div className="mb-3 text-2xl text-blue-400">02</div>
              <h3 className="font-semibold">Clear Reporting</h3>
              <p className="mt-2 text-sm leading-6 text-slate-400">
                Understand findings through clear, prioritised reports.
              </p>
            </div>
          </div>
        </div>

        {/* Login section */}
        <div id="login" className="mx-auto w-full max-w-md">
          <div className="rounded-2xl border border-white/10 bg-[#10213a] p-8 shadow-2xl shadow-black/30 sm:p-10">

            <div className="mb-8">
              <div className="mb-5 flex h-14 w-14 items-center justify-center rounded-xl bg-blue-500/15 text-2xl text-blue-400">
                ◈
              </div>

              <h2 className="text-3xl font-bold">
                Welcome back
              </h2>

              <p className="mt-3 text-sm leading-6 text-slate-400">
                Sign in to access your CyberGuard customer portal.
              </p>
            </div>

            <form className="space-y-6">
              <div>
                <label htmlFor="email" className="mb-2 block text-sm font-medium text-slate-300">
                  Email address
                </label>

                <input
                  id="email"
                  type="email"
                  placeholder="you@company.com"
                  className="w-full rounded-lg border border-white/10 bg-[#071426] px-4 py-3 text-white outline-none transition placeholder:text-slate-600 focus:border-blue-400"
                />
              </div>

              <div>
                <label htmlFor="password" className="mb-2 block text-sm font-medium text-slate-300">
                  Password
                </label>

                <input
                  id="password"
                  type="password"
                  placeholder="Enter your password"
                  className="w-full rounded-lg border border-white/10 bg-[#071426] px-4 py-3 text-white outline-none transition placeholder:text-slate-600 focus:border-blue-400"
                />
              </div>

              <div className="flex items-center justify-between text-sm">
                <label className="flex items-center gap-2 text-slate-400">
                  <input type="checkbox" className="accent-blue-500" />
                  Remember me
                </label>

                <a href="#login" className="text-blue-400 hover:text-blue-300">
                  Forgot password?
                </a>
              </div>

              <button
                type="button"
                className="w-full rounded-lg bg-blue-600 py-3.5 font-semibold transition hover:bg-blue-500"
              >
                Sign In
              </button>
            </form>

            <div className="my-7 border-t border-white/10"></div>

            <p className="text-center text-sm text-slate-400">
              New to CyberGuard?{" "}
              <a href="#register" className="font-semibold text-blue-400 hover:text-blue-300">
                Create an account
              </a>
            </p>

            <div id="register" className="mt-4 text-center text-xs text-slate-500">
              Customer registration will be available as we build the portal.
            </div>
          </div>

          <p className="mt-6 text-center text-xs leading-6 text-slate-500">
            Secure website monitoring starts with informed decisions.
          </p>
        </div>
      </section>

      {/* Footer */}
      <footer id="about" className="border-t border-white/10 px-8 py-8 text-center">
        <p className="text-sm text-slate-400">
          © 2026 MediaRing Computing (Pty) Ltd. All rights reserved.
        </p>
        <p className="mt-2 text-xs text-slate-600">
          MediaRing CyberGuard | Website Security Platform
        </p>
      </footer>

    </main>
  );
}