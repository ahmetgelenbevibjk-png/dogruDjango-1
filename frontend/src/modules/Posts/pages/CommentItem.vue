<script setup>
defineProps({
  comment: Object,
  activeReplyCommentId: [Number, String],
  replyContent: String
});

defineEmits(['toggle-reply', 'update:replyContent', 'submit-reply']);
</script>

<template>
  <div class="comment-item" :class="{ 'reply-item': comment.parent }">
    <div class="comment-user-info">
      <span class="comment-author">{{ comment.username || comment.user?.username || 'Anonim' }}</span>
    </div>
    <p class="comment-body">{{ comment.content }}</p>

    <!-- Yanıtla Butonu -->
    <button @click="$emit('toggle-reply', comment.id)" class="reply-toggle-btn">Yanıtla</button>

    <!-- Alt Yorum Giriş Alanı -->
    <div v-if="activeReplyCommentId === comment.id" class="comment-input-container reply-input-box">
      <input
        :value="replyContent"
        @input="$emit('update:replyContent', $event.target.value)"
        type="text"
        placeholder="Yanıt yaz..."
        @keyup.enter="$emit('submit-reply', comment.id)"
        class="comment-input"
      />
      <button @click="$emit('submit-reply', comment.id)" class="comment-send-btn">Gönder</button>
    </div>

    <!-- Alt Yanıtlar (Recursive - Kendi Kendini Çağırır) -->
    <div v-if="comment.replies && comment.replies.length > 0" class="replies-list">
      <CommentItem
        v-for="reply in comment.replies"
        :key="reply.id"
        :comment="reply"
        :active-reply-comment-id="activeReplyCommentId"
        :reply-content="replyContent"
        @toggle-reply="$emit('toggle-reply', $event)"
        @update:reply-content="$emit('update:replyContent', $event)"
        @submit-reply="$emit('submit-reply', $event)"
      />
    </div>
  </div>
</template>

<style scoped>
.comment-item {
  background: #f7fafc;
  padding: 10px 14px;
  border-radius: 6px;
  margin-bottom: 8px;
}

.comment-author {
  font-weight: 600;
  font-size: 13px;
  color: #2d3748;
  margin-bottom: 4px;
  display: block;
}

.comment-body {
  font-weight: 400;
  font-size: 13px;
  color: #4a5568;
  overflow-wrap: break-word;
  word-break: break-word;
}

.reply-toggle-btn {
  background: none;
  border: none;
  color: #805ad5;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  padding: 4px 0 0 0;
  margin-top: 4px;
}

.reply-toggle-btn:hover {
  text-decoration: underline;
}

.reply-input-box {
  margin-top: 8px;
}

.replies-list {
  margin-left: 15px;
  margin-top: 8px;
  border-left: 2px solid #cbd5e0;
  padding-left: 10px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.reply-item {
  background: #edf2f7;
}

.comment-input-container {
  display: flex;
  gap: 8px;
  align-items: center;
}

.comment-input {
  flex: 1;
  padding: 8px 10px;
  border: 1px solid #cbd5e0;
  border-radius: 6px;
  font-size: 12px;
  outline: none;
}

.comment-send-btn {
  background: #805ad5;
  color: white;
  border: none;
  padding: 8px 12px;
  border-radius: 6px;
  font-weight: 600;
  font-size: 12px;
  cursor: pointer;
}

.comment-send-btn:hover {
  background: #6b46c1;
}
</style>