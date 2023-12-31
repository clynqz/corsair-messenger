﻿using CorsairMessengerServer.Data.Entities.Api.User;
using System.Text.Json.Serialization;

namespace CorsairMessengerServer.Models.Contacts
{
    public class ContactsListResponse
    {
        [JsonRequired]
        [JsonPropertyName("contacts")]
        public required UserResponseEntity[]? Contacts { get; set; }
    }
}
