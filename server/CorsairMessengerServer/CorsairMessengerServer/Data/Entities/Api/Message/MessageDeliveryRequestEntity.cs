﻿using CorsairMessengerServer.Data.Entities.Request.Message;
using System.Text.Json.Serialization;

namespace CorsairMessengerServer.Data.Entities.Request
{
    public class MessageDeliveryRequestEntity : MessageDeliveryBaseEntity
    {
        [JsonPropertyName("receiver_id")]
        public int ReceiverId { get; set; }

        [JsonPropertyName("text")]
        public string? Text { get; set; }
    }
}
