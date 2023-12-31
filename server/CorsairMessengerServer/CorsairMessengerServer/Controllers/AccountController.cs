﻿using CorsairMessengerServer.Data.Entities;
using CorsairMessengerServer.Data.Repositories;
using CorsairMessengerServer.Extensions;
using CorsairMessengerServer.Helpers;
using CorsairMessengerServer.Models.Auth;
using CorsairMessengerServer.Models.Register;
using CorsairMessengerServer.Services.PasswordHasher;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Caching.Distributed;
using Microsoft.IdentityModel.Tokens;
using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using static CorsairMessengerServer.Data.Constraints.UserEntityConstraints;

namespace CorsairMessengerServer.Controllers
{
    [Authorize]
    [ApiController]
    [Route("account")]
    public class AccountController : ControllerBase
    {
        private const int AUTH_TOKEN_LIFETIME_MINUTES = 365 * 24 * 60;

        private readonly UsersRepository _usersRepository;

        private readonly IDistributedCache _cache;

        public AccountController(UsersRepository userRepository, IDistributedCache cache)
        {
            _usersRepository = userRepository;
            _cache = cache;
        }

        [HttpGet("validate")]
        public ActionResult Validate()
        {
            return Ok();
        }

        //[HttpPost("change-password")]
        //public async Task<ActionResult<AuthResponse>> ChangePasswordAsync([FromBody] AuthRequest request, [FromServices] IPasswordHasher hasher)
        //{
        //    return BadRequest();
        //}

        [AllowAnonymous]
        [HttpPost("login")]
        public async Task<ActionResult<AuthResponse>> LoginAsync([FromBody] AuthRequest request, [FromServices] IPasswordHasher hasher)
        {
            var user = await _usersRepository.GetUserByLoginAsync(request.Login, true);

            if (user is null)
            {
                return BadRequest(new { Field = "login" });
            }

            var verified = hasher.Verify(request.Password, user.Password!);

            if (!verified)
            {
                return BadRequest(new { Field = "password" });
            }

            var token = await GetAuthTokenAsync(user);

            var response = new AuthResponse
            {
                Token = token,
            };

            return Ok(response);
        }

        [AllowAnonymous]
        [HttpPost("register")]
        public async Task<ActionResult<AuthResponse>> RegisterAsync([FromBody] RegisterRequest request, [FromServices] IPasswordHasher hasher)
        {
            var nickname = request.Nickname;
            var email = request.Email;
            var password = request.Password;

            if (!password.Length.InRange(PASSWORD_MIN_LENGTH, PASSWORD_MAX_LENGTH))
            {
                return BadRequest(new { Field = nameof(password) });
            }

            var isNicknameExist = await _usersRepository.IsNicknameExistAsync(nickname);

            if (isNicknameExist)
            {
                return Conflict(new { Field = nameof(nickname) });
            }

            var isEmailExist = await _usersRepository.IsEmailExistAsync(email);

            if (isEmailExist)
            {
                return Conflict(new { Field = nameof(nickname) });
            }

            var user = CreateUser(nickname, email, password, hasher);

            await _usersRepository.AddUserAsync(user);

            var token = await GetAuthTokenAsync(user);

            var response = new AuthResponse
            {
                Token = token,
            };

            return Ok(response);
        }

        private static UserEntity CreateUser(string nickname, string email, string password, IPasswordHasher hasher)
        {
            var hashedPassword = hasher.Hash(password);

            return new UserEntity { Nickname = nickname, Email = email, Password = hashedPassword };
        }

        private async Task<string> GetAuthTokenAsync(UserEntity user)
        {
            var userId = user.Id.ToString();
            var sessionId = Guid.NewGuid().ToString();

            var claims = new List<Claim>
            {
                new(ClaimTypes.NameIdentifier, userId),
                new(ClaimTypes.Sid, sessionId),
            };

            var jwt = new JwtSecurityToken(
                    claims: claims,
                    signingCredentials: new SigningCredentials(AuthOptions.SymmetricSecurityKey, SecurityAlgorithms.HmacSha256));

            var token = new JwtSecurityTokenHandler().WriteToken(jwt);

            await RegisterSession(userId, sessionId);

            return token;
        }

        private async Task RegisterSession(string userId, string sessionId)
        {
            await _cache.SetStringAsync(userId, sessionId, new DistributedCacheEntryOptions
            {
                AbsoluteExpirationRelativeToNow = TimeSpan.FromMinutes(AUTH_TOKEN_LIFETIME_MINUTES),
            });
        }
    }
}
