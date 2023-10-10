﻿using System.Collections.Concurrent;
using System.Net.WebSockets;

namespace CorsairMessengerServer.Data.Repositories.WebSockets
{
    public class WebSocketsRepository : IWebSocketsRepository
    {
        private static readonly ConcurrentDictionary<int, WebSocket> _connectedWebSockets;

        static WebSocketsRepository()
        {
            _connectedWebSockets = new ConcurrentDictionary<int, WebSocket>();
        }

        public void AddWebSocket(int socketId, WebSocket webSocket)
        {
            _connectedWebSockets[socketId] = webSocket;
        }

        public bool TryGetWebSocket(int socketId, out WebSocket webSocket)
        {
            return _connectedWebSockets.TryGetValue(socketId, out webSocket!);
        }

        public async Task RemoveWebSocket(int socketId)
        {
            if (_connectedWebSockets.TryRemove(socketId, out var webSocket))
            {
                await webSocket.CloseAsync(WebSocketCloseStatus.NormalClosure, "Web socket close requested", CancellationToken.None);
            }
        }
    }
}
