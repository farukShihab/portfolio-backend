import requests

TIMEOUT = 20
UA = {"User-Agent": "Mozilla/5.0 (portfolio-stats-bot)"}


def codeforces(handle):
    info = requests.get("https://codeforces.com/api/user.info",
                        params={"handles": handle}, timeout=TIMEOUT).json()
    if info["status"] != "OK":
        raise RuntimeError(info.get("comment", "CF user.info failed"))
    u = info["result"][0]

    subs = requests.get("https://codeforces.com/api/user.status",
                        params={"handle": handle}, timeout=TIMEOUT).json()
    solved = {
        (s["problem"].get("contestId"), s["problem"]["index"], s["problem"]["name"])
        for s in subs["result"] if s.get("verdict") == "OK"
    }
    return {
        "rating": u.get("rating"),
        "max_rating": u.get("maxRating"),
        "solved": len(solved),
        "profile_url": f"https://codeforces.com/profile/{handle}",
    }


def atcoder(handle):
    # Rating history: public JSON on atcoder.jp
    hist = requests.get(f"https://atcoder.jp/users/{handle}/history/json",
                        headers=UA, timeout=TIMEOUT).json()
    rating = hist[-1]["NewRating"] if hist else None
    max_rating = max((h["NewRating"] for h in hist), default=None)

    # Solve count: community API (kenkoooo AtCoder Problems)
    ac = requests.get("https://kenkoooo.com/atcoder/atcoder-api/v3/user/ac_rank",
                      params={"user": handle}, headers=UA, timeout=TIMEOUT).json()
    return {
        "rating": rating,
        "max_rating": max_rating,
        "solved": ac["count"],
        "profile_url": f"https://atcoder.jp/users/{handle}",
    }


LC_QUERY = """
query($u: String!) {
  matchedUser(username: $u) {
    submitStats { acSubmissionNum { difficulty count } }
  }
  userContestRanking(username: $u) { rating }
}"""

def leetcode(handle):
    r = requests.post(
        "https://leetcode.com/graphql",
        json={"query": LC_QUERY, "variables": {"u": handle}},
        headers={**UA, "Referer": f"https://leetcode.com/u/{handle}/"},
        timeout=TIMEOUT,
    ).json()["data"]
    if not r["matchedUser"]:
        raise RuntimeError("LeetCode user not found")
    solved = next(x["count"] for x in
                  r["matchedUser"]["submitStats"]["acSubmissionNum"]
                  if x["difficulty"] == "All")
    contest = r.get("userContestRanking")
    rating = round(contest["rating"]) if contest else None
    return {
        "rating": rating,
        "max_rating": None,
        "solved": solved,
        "profile_url": f"https://leetcode.com/u/{handle}/",
    }