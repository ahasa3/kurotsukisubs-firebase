// ===========================
// Kurotsukisubs - Post Data
// ===========================

const POSTS_PER_PAGE = 5;

const posts = [
  {
    id: 1,
    title: "Nogizaka46 – 35th Single 'Chigau Ball wo Keruна' MV",
    excerpt: "The music video for Nogizaka46's 35th single has been subbed! Featuring the center Yamashita Mizuki with a stunning choreography and emotional storyline.",
    content: `<p>We are thrilled to present the fully subbed music video for Nogizaka46's 35th single <strong>"Chigau Ball wo Keru"</strong>. This single marks a significant milestone for the group, featuring Yamashita Mizuki as the center for the third consecutive time.</p>
    <p>The music video was filmed over three days in Hokkaido, capturing the breathtaking winter landscapes that perfectly complement the song's emotional depth. The choreography, designed by renowned choreographer Takahashi Yuki, incorporates elements of classical ballet with modern pop dance.</p>
    <h3>About the Song</h3>
    <p>The lyrics, penned by Akimoto Yasushi, explore themes of perseverance and chasing dreams even when the path seems unclear. The title, which roughly translates to "Kicking a Different Ball," is a metaphor for taking unconventional paths in life.</p>
    <p>Translation notes: Several idiomatic expressions were particularly challenging to localize. We've included translator notes in the subtitle file for context on cultural references.</p>`,
    member: "Yamashita Mizuki",
    memberInitials: "YM",
    date: "2026-02-28",
    tags: ["MV", "Subbed"],
    type: "subbed",
    emoji: "🎵",
    downloads: [
      { name: "720p MKV (Soft Subs)", size: "1.2 GB", url: "#" },
      { name: "1080p MKV (Soft Subs)", size: "2.4 GB", url: "#" },
      { name: "Subtitle File (.ass)", size: "48 KB", url: "#" }
    ]
  },
  {
    id: 2,
    title: "Nogizaka46 – Nogizaka Skits Vol.12 Episode 3",
    excerpt: "The latest episode of Nogizaka Skits is here! This week features Ikuta Erika and Hori Miona in a hilarious cooking challenge that goes completely off the rails.",
    content: `<p>Episode 3 of Nogizaka Skits Vol.12 is now available with full English subtitles! This episode is an absolute treat for fans of Ikuta Erika and Hori Miona, as the two veteran members team up for a cooking challenge that quickly devolves into chaos.</p>
    <p>The episode runs approximately 24 minutes and features several recurring segments including the fan-favorite "Member Trivia Quiz" and a new segment called "Nogi Kitchen" where members attempt to recreate traditional Japanese dishes.</p>
    <h3>Translation Notes</h3>
    <p>This episode contained several puns and wordplay that were particularly challenging to translate. We've done our best to preserve the humor while making it accessible to international fans. Some jokes have been adapted for cultural context.</p>
    <p>Special thanks to our translation team for their hard work on this episode, especially the rapid-fire dialogue sections!</p>`,
    member: "Ikuta Erika",
    memberInitials: "IE",
    date: "2026-02-21",
    tags: ["Variety", "Subbed"],
    type: "subbed",
    emoji: "🎭",
    downloads: [
      { name: "720p MP4 (Soft Subs)", size: "680 MB", url: "#" },
      { name: "Subtitle File (.srt)", size: "32 KB", url: "#" }
    ]
  },
  {
    id: 3,
    title: "Nogizaka46 – 5th Year Birthday Live Day 2 [RAW]",
    excerpt: "RAW footage of the 5th Year Birthday Live Day 2 concert. Full concert with all performances. Subbed version coming soon — translators needed!",
    content: `<p>We are releasing the RAW (unsubtitled) footage of Nogizaka46's 5th Year Birthday Live Day 2 concert. This is a full concert recording featuring all performances from the event held at Meiji Jingu Stadium.</p>
    <p>The concert featured performances of over 30 songs spanning the group's entire discography, including rare performances of early singles and special unit stages.</p>
    <h3>Setlist Highlights</h3>
    <p>Notable performances include the full debut of the new 4th generation unit stage, a surprise appearance by graduated members, and an emotional encore performance of "Kimi no Na wa Kibou."</p>
    <p><strong>Note:</strong> This is a RAW release. We are actively looking for translators to help subtitle this concert. If you are interested in joining our team, please visit our Discord server.</p>`,
    member: "Various Members",
    memberInitials: "VM",
    date: "2026-02-14",
    tags: ["Concert", "RAW"],
    type: "raw",
    emoji: "🎤",
    downloads: [
      { name: "1080p MKV (RAW)", size: "8.6 GB", url: "#" },
      { name: "720p MKV (RAW)", size: "4.2 GB", url: "#" }
    ]
  },
  {
    id: 4,
    title: "Nogizaka46 – Nogizaka Under Construction Ep.342",
    excerpt: "Episode 342 of the beloved variety show is now subbed! This week's episode features a special 'Nogi Olympics' segment with hilarious athletic challenges.",
    content: `<p>Episode 342 of Nogizaka Under Construction is now available with full English subtitles! This week's theme is the "Nogi Olympics," a special segment where members compete in various athletic and skill-based challenges.</p>
    <p>Highlights include Sato Kaede's surprisingly impressive archery skills, Kubo Shiori's complete failure at the balance beam challenge (in the most entertaining way possible), and a nail-biting final relay race that had the studio audience on their feet.</p>
    <h3>Featured Members</h3>
    <p>This episode features a large cast including Sato Kaede, Kubo Shiori, Yoda Yuki, Tamura Mayu, and many more. The episode runs 48 minutes including the post-show segment.</p>
    <p>Translation quality check was performed by two of our senior translators to ensure accuracy of the sports commentary and member banter.</p>`,
    member: "Sato Kaede",
    memberInitials: "SK",
    date: "2026-02-07",
    tags: ["Variety", "Subbed"],
    type: "subbed",
    emoji: "📺",
    downloads: [
      { name: "720p MP4 (Soft Subs)", size: "920 MB", url: "#" },
      { name: "1080p MP4 (Soft Subs)", size: "1.8 GB", url: "#" },
      { name: "Subtitle File (.ass)", size: "56 KB", url: "#" }
    ]
  },
  {
    id: 5,
    title: "Nogizaka46 – 'Influencer' Dance Practice Video",
    excerpt: "The iconic 'Influencer' dance practice video has been subbed with full translation of the choreography notes and member commentary.",
    content: `<p>We've subbed the dance practice video for one of Nogizaka46's most iconic songs, "Influencer." This video includes the full choreography practice session with member commentary and choreographer notes.</p>
    <p>The video provides a fascinating behind-the-scenes look at how the complex formation changes in "Influencer" were developed and rehearsed. The choreography for this song is considered one of the most technically demanding in the group's history.</p>
    <h3>Choreography Notes</h3>
    <p>The dance features 47 formation changes in just over 4 minutes, requiring precise timing and coordination from all members. The practice video shows the step-by-step process of learning these formations.</p>
    <p>Member commentary has been fully translated, including Shiraishi Mai's detailed explanation of the center position challenges and Nishino Nanase's thoughts on the emotional expression required for the performance.</p>`,
    member: "Shiraishi Mai",
    memberInitials: "SM",
    date: "2026-01-31",
    tags: ["Dance", "Subbed"],
    type: "subbed",
    emoji: "💃",
    downloads: [
      { name: "1080p MP4 (Soft Subs)", size: "1.1 GB", url: "#" },
      { name: "Subtitle File (.srt)", size: "28 KB", url: "#" }
    ]
  },
  {
    id: 6,
    title: "Nogizaka46 – Nogizaka Skits Vol.12 Episode 2",
    excerpt: "Episode 2 of Nogizaka Skits Vol.12 features the 4th generation members in a hilarious escape room challenge. Watch them struggle (and succeed!) together.",
    content: `<p>Episode 2 of Nogizaka Skits Vol.12 is now available! This episode focuses on the 4th generation members as they tackle an elaborate escape room challenge designed specifically for the show.</p>
    <p>The escape room features Nogizaka46-themed puzzles and clues, making it both entertaining for fans and a genuine challenge for the members. The episode captures genuine moments of frustration, teamwork, and triumph.</p>
    <h3>4th Generation Spotlight</h3>
    <p>This episode is a great opportunity to get to know the 4th generation members better, as the escape room format naturally brings out their personalities and problem-solving styles.</p>`,
    member: "Yamoto Rika",
    memberInitials: "YR",
    date: "2026-01-24",
    tags: ["Variety", "Subbed"],
    type: "subbed",
    emoji: "🎭",
    downloads: [
      { name: "720p MP4 (Soft Subs)", size: "710 MB", url: "#" },
      { name: "Subtitle File (.srt)", size: "35 KB", url: "#" }
    ]
  },
  {
    id: 7,
    title: "Nogizaka46 – 34th Single 'Kakehiki wa Iranai' MV",
    excerpt: "The music video for the 34th single 'Kakehiki wa Iranai' is now fully subbed. A beautiful and melancholic MV featuring Kubo Shiori as center.",
    content: `<p>We present the fully subbed music video for Nogizaka46's 34th single <strong>"Kakehiki wa Iranai"</strong> (No Need for Games). This single features Kubo Shiori as center, marking her first time in the center position for a major single.</p>
    <p>The music video was filmed in a stunning European-style mansion and features a narrative about unrequited love and the courage to be honest about one's feelings. The cinematography is particularly noteworthy, with each scene carefully composed to reflect the emotional state of the protagonist.</p>
    <h3>Translation Notes</h3>
    <p>The title "Kakehiki wa Iranai" is a nuanced phrase that can mean both "no need for games/tactics" and "no need for negotiations," reflecting the song's theme of honest, straightforward love.</p>`,
    member: "Kubo Shiori",
    memberInitials: "KS",
    date: "2026-01-17",
    tags: ["MV", "Subbed"],
    type: "subbed",
    emoji: "🎵",
    downloads: [
      { name: "1080p MKV (Soft Subs)", size: "2.1 GB", url: "#" },
      { name: "720p MKV (Soft Subs)", size: "1.0 GB", url: "#" },
      { name: "Subtitle File (.ass)", size: "42 KB", url: "#" }
    ]
  },
  {
    id: 8,
    title: "Nogizaka46 – Nogizaka Under Construction Ep.341",
    excerpt: "Episode 341 features a special 'Nogi Cooking Battle' where members compete to create the best bento box. Featuring Tamura Mayu's surprisingly impressive culinary skills!",
    content: `<p>Episode 341 of Nogizaka Under Construction is now available with full English subtitles! This week's theme is the "Nogi Cooking Battle," where members compete to create the most delicious and visually appealing bento box.</p>
    <p>The episode is filled with cooking disasters, unexpected successes, and plenty of member banter. Tamura Mayu emerges as a surprise culinary talent, while Yoda Yuki's attempt at tamagoyaki becomes the episode's most memorable moment.</p>`,
    member: "Tamura Mayu",
    memberInitials: "TM",
    date: "2026-01-10",
    tags: ["Variety", "Subbed"],
    type: "subbed",
    emoji: "📺",
    downloads: [
      { name: "720p MP4 (Soft Subs)", size: "880 MB", url: "#" },
      { name: "Subtitle File (.ass)", size: "52 KB", url: "#" }
    ]
  },
  {
    id: 9,
    title: "Nogizaka46 – New Year Special Live 2026 [RAW]",
    excerpt: "RAW footage of the New Year Special Live 2026. A special concert celebrating the new year with classic songs and new performances.",
    content: `<p>We are releasing the RAW footage of Nogizaka46's New Year Special Live 2026. This special concert was held on January 1st, 2026, and featured a mix of classic songs and new performances to celebrate the new year.</p>
    <p>The concert featured special costumes designed exclusively for the new year celebration, and included a midnight countdown segment that was broadcast live on national television.</p>
    <p><strong>Note:</strong> This is a RAW release without subtitles. A subbed version is in progress.</p>`,
    member: "Various Members",
    memberInitials: "VM",
    date: "2026-01-03",
    tags: ["Concert", "RAW"],
    type: "raw",
    emoji: "🎆",
    downloads: [
      { name: "1080p MKV (RAW)", size: "6.8 GB", url: "#" },
      { name: "720p MKV (RAW)", size: "3.4 GB", url: "#" }
    ]
  },
  {
    id: 10,
    title: "Nogizaka46 – 'Yubi Bouenkyou' Acoustic Version",
    excerpt: "A rare acoustic version of the classic 'Yubi Bouenkyou' performed by Hashimoto Nanami and Nishino Nanase at a special fan event.",
    content: `<p>We've subbed a rare acoustic performance of "Yubi Bouenkyou" (Finger Telescope) performed by Hashimoto Nanami and Nishino Nanase at a special fan appreciation event. This intimate performance strips away the production elements to reveal the raw emotional power of the song.</p>
    <p>The performance was accompanied only by acoustic guitar and piano, allowing the vocal harmonies between Hashimoto and Nishino to take center stage. This is considered one of the most treasured fan recordings in the Nogizaka46 community.</p>
    <h3>Historical Context</h3>
    <p>"Yubi Bouenkyou" was originally released as a coupling track on the 14th single and has since become one of the most beloved songs in the group's catalog, often cited by members as their personal favorite.</p>`,
    member: "Hashimoto Nanami",
    memberInitials: "HN",
    date: "2025-12-27",
    tags: ["Performance", "Subbed"],
    type: "subbed",
    emoji: "🎸",
    downloads: [
      { name: "720p MP4 (Soft Subs)", size: "420 MB", url: "#" },
      { name: "Subtitle File (.srt)", size: "22 KB", url: "#" }
    ]
  },
  {
    id: 11,
    title: "Nogizaka46 – Nogizaka Skits Vol.12 Episode 1",
    excerpt: "The first episode of Nogizaka Skits Vol.12 kicks off with a bang! A hilarious game show parody featuring the senior members.",
    content: `<p>We're excited to kick off our coverage of Nogizaka Skits Vol.12 with the first episode! This episode features a game show parody where senior members compete in increasingly absurd challenges.</p>
    <p>The episode sets the tone for the entire volume with its blend of physical comedy, wordplay, and genuine member chemistry. Highlights include Ikuta Erika's dramatic overacting in the acting challenge and Shiraishi Mai's surprisingly competitive nature in the trivia segment.</p>`,
    member: "Ikuta Erika",
    memberInitials: "IE",
    date: "2025-12-20",
    tags: ["Variety", "Subbed"],
    type: "subbed",
    emoji: "🎭",
    downloads: [
      { name: "720p MP4 (Soft Subs)", size: "650 MB", url: "#" },
      { name: "Subtitle File (.srt)", size: "38 KB", url: "#" }
    ]
  },
  {
    id: 12,
    title: "Nogizaka46 – Christmas Special 2025 [RAW]",
    excerpt: "RAW footage of the Christmas Special 2025 live performance. Features special holiday costumes and a surprise medley of Christmas-themed songs.",
    content: `<p>We are releasing the RAW footage of Nogizaka46's Christmas Special 2025. This special event was held on December 24th, 2025, and featured the members in special holiday costumes performing a mix of original songs and Christmas classics.</p>
    <p>The event included a special segment where members shared their Christmas wishes and memories, as well as a surprise medley of holiday songs arranged in Nogizaka46's signature style.</p>
    <p><strong>Note:</strong> This is a RAW release. Subtitles are being worked on.</p>`,
    member: "Various Members",
    memberInitials: "VM",
    date: "2025-12-25",
    tags: ["Concert", "RAW"],
    type: "raw",
    emoji: "🎄",
    downloads: [
      { name: "1080p MKV (RAW)", size: "5.2 GB", url: "#" },
      { name: "720p MKV (RAW)", size: "2.6 GB", url: "#" }
    ]
  }
];

// ===========================
// Utility Functions
// ===========================

function formatDate(dateStr) {
  const date = new Date(dateStr);
  return date.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
}

function getPostById(id) {
  return posts.find(p => p.id === parseInt(id));
}

function getPaginatedPosts(page = 1, perPage = POSTS_PER_PAGE) {
  const start = (page - 1) * perPage;
  const end = start + perPage;
  return {
    posts: posts.slice(start, end),
    total: posts.length,
    totalPages: Math.ceil(posts.length / perPage),
    currentPage: page
  };
}

function getMemberStats() {
  const memberMap = {};
  posts.forEach(post => {
    if (!memberMap[post.member]) {
      memberMap[post.member] = { name: post.member, initials: post.memberInitials, count: 0 };
    }
    memberMap[post.member].count++;
  });
  return Object.values(memberMap).sort((a, b) => b.count - a.count);
}

// ===========================
// Render Functions
// ===========================

function renderPostCard(post) {
  return `
    <a class="post-card" href="posts.html?id=${post.id}" onclick="return navigateToPost(${post.id})">
      <div class="post-thumbnail-placeholder">
        <span style="position:relative;z-index:1;">${post.emoji}</span>
      </div>
      <div class="post-body">
        <div class="post-meta">
          <span class="post-tag ${post.type}">${post.tags[0]}</span>
          ${post.tags[1] ? `<span class="post-tag ${post.type}">${post.tags[1]}</span>` : ''}
          <span class="post-date">${formatDate(post.date)}</span>
        </div>
        <h3 class="post-title">${post.title}</h3>
        <p class="post-excerpt">${post.excerpt}</p>
      </div>
      <div class="post-footer">
        <div class="post-member">
          <div class="member-avatar">${post.memberInitials}</div>
          <span class="member-name">${post.member}</span>
        </div>
        <span class="post-read-more">Read more →</span>
      </div>
    </a>
  `;
}

function renderPagination(currentPage, totalPages, onPageChange) {
  if (totalPages <= 1) return '';

  let html = '<div class="pagination">';

  // Prev button
  html += `<button class="page-btn" onclick="${onPageChange}(${currentPage - 1})" ${currentPage === 1 ? 'disabled' : ''}>‹</button>`;

  // Page numbers
  for (let i = 1; i <= totalPages; i++) {
    if (
      i === 1 ||
      i === totalPages ||
      (i >= currentPage - 1 && i <= currentPage + 1)
    ) {
      html += `<button class="page-btn ${i === currentPage ? 'active' : ''}" onclick="${onPageChange}(${i})">${i}</button>`;
    } else if (i === currentPage - 2 || i === currentPage + 2) {
      html += `<button class="page-btn" disabled>…</button>`;
    }
  }

  // Next button
  html += `<button class="page-btn" onclick="${onPageChange}(${currentPage + 1})" ${currentPage === totalPages ? 'disabled' : ''}>›</button>`;

  html += '</div>';
  return html;
}

function renderSakuraPetals() {
  const container = document.querySelector('.hero-sakura');
  if (!container) return;
  for (let i = 0; i < 12; i++) {
    const petal = document.createElement('div');
    petal.className = 'petal';
    petal.style.left = Math.random() * 100 + '%';
    petal.style.animationDuration = (Math.random() * 8 + 6) + 's';
    petal.style.animationDelay = (Math.random() * 10) + 's';
    petal.style.width = (Math.random() * 6 + 4) + 'px';
    petal.style.height = petal.style.width;
    container.appendChild(petal);
  }
}

function navigateToPost(id) {
  window.location.href = `posts.html?id=${id}`;
  return false;
}
